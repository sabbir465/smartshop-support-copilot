import json
import os
from typing import Annotated, Literal, TypedDict

from dotenv import load_dotenv
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph, add_messages

from tools import (
    evaluate_refund as evaluate_refund_function,
    find_customer_by_email as find_customer_function,
    find_order as find_order_function,
    get_refund_policy as get_refund_policy_function,
)
import time
from metrics import (
    AGENT_EXECUTION_DURATION_SECONDS,
    AGENT_TOOL_CALLS_TOTAL,
    AGENT_TOOL_ERRORS_TOTAL,
    LLM_CALLS_TOTAL,
    LLM_ERRORS_TOTAL,
    POLICY_ENFORCEMENTS_TOTAL,
    REFUND_DECISIONS_TOTAL,
)

load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")


SYSTEM_PROMPT = """
You are an AI Customer Support Agent for an e-commerce company.

Rules:
1. Use tools to inspect customer information, order information, and policy.
2. Never invent customer or order information.
3. A formal refund decision must come from evaluate_refund.
4. You must follow the evaluate_refund decision exactly.
5. If the policy denies a request, politely hold the line.
6. Customer tier cannot override strict policy restrictions.
7. Produce a concise and empathetic customer-facing response.
8. If a customer or order lookup returns an error, do not infer or invent any missing information.
9. Never describe an item, category, amount, condition, or policy outcome unless it was returned by a tool.
"""


class AgentState(TypedDict):
    """
    Shared information passed between LangGraph nodes.
    """

    messages: Annotated[list[BaseMessage], add_messages]
    logs: list[dict[str, str]]
    current_order_id: str | None
    final_decision: str | None
    lookup_error: str | None
    iterations: int


@tool("find_customer_by_email")
def find_customer_by_email_tool(email: str) -> dict:
    """Find a customer CRM profile using the customer's email address."""

    return find_customer_function(email)


@tool("find_order")
def find_order_tool(order_id: str) -> dict:
    """Retrieve an e-commerce order using its order ID."""

    return find_order_function(order_id)


@tool("get_refund_policy")
def get_refund_policy_tool() -> str:
    """Retrieve the strict e-commerce refund policy."""

    return get_refund_policy_function()


@tool("evaluate_refund")
def evaluate_refund_tool(order_id: str) -> dict:
    """Apply deterministic refund rules and return the formal decision."""

    return evaluate_refund_function(order_id)


TOOLS = [
    find_customer_by_email_tool,
    find_order_tool,
    get_refund_policy_tool,
    evaluate_refund_tool,
]

TOOLS_BY_NAME = {tool_definition.name: tool_definition for tool_definition in TOOLS}


model = ChatOpenAI(
    model=MODEL_NAME,
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0,
)

model_with_tools = model.bind_tools(TOOLS)



def agent_node(state: AgentState) -> dict:
    """
    Ask the LLM whether it should call another tool or provide a final answer.
    """

    LLM_CALLS_TOTAL.inc()

    try:
        response = model_with_tools.invoke(
            [
                SystemMessage(content=SYSTEM_PROMPT),
                *state["messages"],
            ]
        )
    except Exception:
        LLM_ERRORS_TOTAL.inc()
        raise

    return {
        "messages": [response],
        "iterations": state["iterations"] + 1,
    }


def tool_node(state: AgentState) -> dict:
    """
    Execute every tool requested by the most recent AI message.

    This custom tool node captures:
    - execution logs,
    - current order ID,
    - final refund decision,
    - lookup failures,
    - Prometheus tool metrics.
    """

    last_message = state["messages"][-1]

    if not isinstance(last_message, AIMessage):
        raise ValueError(
            "The tool node expected the latest message to be AIMessage."
        )

    logs = list(state["logs"])
    tool_messages: list[ToolMessage] = []

    current_order_id = state["current_order_id"]
    final_decision = state["final_decision"]
    lookup_error = state["lookup_error"]

    for tool_call in last_message.tool_calls:
        tool_name = tool_call["name"]
        tool_arguments = tool_call.get("args", {})

        AGENT_TOOL_CALLS_TOTAL.labels(tool=tool_name).inc()

        selected_tool = TOOLS_BY_NAME.get(tool_name)

        logs.append(
            {
                "step": f"Planning tool call: {tool_name}",
                "detail": (
                    f"Agent selected `{tool_name}` with arguments: "
                    f"{json.dumps(tool_arguments)}"
                ),
            }
        )

        if selected_tool is None:
            AGENT_TOOL_ERRORS_TOTAL.labels(tool=tool_name).inc()

            result = {
                "error": f"Unknown tool: {tool_name}",
            }
        else:
            try:
                result = selected_tool.invoke(tool_arguments)
            except Exception as exc:
                AGENT_TOOL_ERRORS_TOTAL.labels(tool=tool_name).inc()

                result = {
                    "error": "Tool execution failed",
                    "detail": str(exc),
                }

        if tool_name == "find_customer_by_email" and isinstance(result, dict):
            if "error" in result:
                requested_email = tool_arguments.get("email", "provided email")
                lookup_error = (
                    f"No customer profile was found for {requested_email}."
                )

        if tool_name == "find_order" and isinstance(result, dict):
            if "error" in result:
                requested_order_id = tool_arguments.get(
                    "order_id",
                    "the provided order ID",
                )

                lookup_error = (
                    f"Order {requested_order_id} was not found in the CRM."
                )
            else:
                current_order_id = result.get("order_id")

        if tool_name == "evaluate_refund" and isinstance(result, dict):
            final_decision = result.get("decision")

        if tool_name == "get_refund_policy":
            display_result = (
                "Refund policy loaded successfully. "
                "The agent will validate the refund window, item category, "
                "item condition, customer risk status, and customer tier."
            )
        else:
            display_result = json.dumps(result, indent=2)

        logs.append(
            {
                "step": f"Tool result received: {tool_name}",
                "detail": display_result,
            }
        )

        tool_messages.append(
            ToolMessage(
                content=json.dumps(result),
                tool_call_id=tool_call["id"],
                name=tool_name,
            )
        )

    return {
        "messages": tool_messages,
        "logs": logs,
        "current_order_id": current_order_id,
        "final_decision": final_decision,
        "lookup_error": lookup_error,
    }



def lookup_failure_node(state: AgentState) -> dict:
    """
    Produce a deterministic response when a required CRM record
    cannot be found.

    This prevents the LLM from inventing customer, order, or policy details.
    """

    lookup_error = (
        state["lookup_error"]
        or "The requested customer or order record could not be verified."
    )

    logs = [
        *state["logs"],
        {
            "step": "Request validation failed",
            "detail": lookup_error,
        },
    ]

    response = AIMessage(
        content=(
            f"{lookup_error} Please verify the email address and order ID "
            "and submit the request again. I cannot approve or evaluate a "
            "refund without a valid CRM record."
        )
    )

    return {
        "messages": [response],
        "logs": logs,
        "final_decision": "deny",
    }



def enforce_policy_node(state: AgentState) -> dict:
    """
    Run deterministic policy evaluation when the LLM attempts to finish
    without calling evaluate_refund.
    """

    order_id = state["current_order_id"]

    if not order_id:
        return {}

    POLICY_ENFORCEMENTS_TOTAL.inc()

    evaluation_result = evaluate_refund_function(order_id)

    logs = [
        *state["logs"],
        {
            "step": "Required policy evaluation",
            "detail": (
                "The model attempted to finish before formal policy "
                "evaluation. The backend enforced deterministic validation "
                f"for order {order_id}."
            ),
        },
        {
            "step": "Tool result received: evaluate_refund",
            "detail": json.dumps(evaluation_result, indent=2),
        },
    ]

    policy_message = HumanMessage(
        content=(
            "A required deterministic policy evaluation was completed by "
            f"the backend. Result: {json.dumps(evaluation_result)}. "
            "Write the final customer-facing response and follow this "
            "decision exactly. Do not request an exception and do not "
            "call more tools."
        )
    )

    return {
        "messages": [policy_message],
        "logs": logs,
        "final_decision": evaluation_result.get("decision"),
    }



def route_after_agent(
    state: AgentState,
) -> Literal["tools", "enforce_policy", "__end__"]:
    """
    Decide where the workflow goes after an LLM response.
    """

    last_message = state["messages"][-1]

    if isinstance(last_message, AIMessage) and last_message.tool_calls:
        return "tools"

    if state["final_decision"] is None and state["current_order_id"]:
        return "enforce_policy"

    return END



def route_after_tools(
    state: AgentState,
) -> Literal["agent", "lookup_failure"]:
    """
    Stop normal agent execution when a required CRM lookup fails.
    """

    if state["lookup_error"]:
        return "lookup_failure"

    return "agent"


def build_graph():
    """
    Construct and compile the LangGraph workflow.
    """

    workflow = StateGraph(AgentState)

    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", tool_node)
    workflow.add_node("lookup_failure", lookup_failure_node)
    workflow.add_node("enforce_policy", enforce_policy_node)

    workflow.add_edge(START, "agent")

    workflow.add_conditional_edges(
        "agent",
        route_after_agent,
        {
            "tools": "tools",
            "enforce_policy": "enforce_policy",
            END: END,
        },
    )

    workflow.add_conditional_edges(
        "tools",
        route_after_tools,
        {
            "agent": "agent",
            "lookup_failure": "lookup_failure",
        },
    )

    workflow.add_edge("lookup_failure", END)
    workflow.add_edge("enforce_policy", "agent")

    return workflow.compile()



refund_graph = build_graph()



def run_graph_agent(user_message: str) -> dict:
    """
    Invoke the LangGraph agent while preserving the existing /chat response.

    Prometheus metrics capture:
    - total agent execution duration,
    - final refund decision.
    """

    start_time = time.perf_counter()

    initial_state: AgentState = {
        "messages": [HumanMessage(content=user_message)],
        "logs": [],
        "current_order_id": None,
        "final_decision": None,
        "lookup_error": None,
        "iterations": 0,
    }

    try:
        result = refund_graph.invoke(
            initial_state,
            config={"recursion_limit": 15},
        )
    finally:
        AGENT_EXECUTION_DURATION_SECONDS.observe(
            time.perf_counter() - start_time
        )

    final_answer = (
        "I’m sorry, but I could not complete the refund review. "
        "A customer-support specialist will need to review it."
    )

    for message in reversed(result["messages"]):
        if isinstance(message, AIMessage) and message.content:
            final_answer = str(message.content)
            break

    final_decision = result.get("final_decision")

    if final_decision:
        REFUND_DECISIONS_TOTAL.labels(
            decision=final_decision
        ).inc()

    return {
        "answer": final_answer,
        "decision": final_decision,
        "logs": result.get("logs", []),
    }