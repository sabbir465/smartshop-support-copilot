import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from tools import find_customer_by_email, find_order, get_refund_policy, evaluate_refund

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "find_customer_by_email",
            "description": "Find a customer profile by email.",
            "parameters": {
                "type": "object",
                "properties": {"email": {"type": "string"}},
                "required": ["email"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "find_order",
            "description": "Find order details by order ID.",
            "parameters": {
                "type": "object",
                "properties": {"order_id": {"type": "string"}},
                "required": ["order_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_refund_policy",
            "description": "Retrieve the strict refund policy.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "evaluate_refund",
            "description": "Evaluate refund eligibility using strict policy rules.",
            "parameters": {
                "type": "object",
                "properties": {"order_id": {"type": "string"}},
                "required": ["order_id"],
            },
        },
    },
]


TOOL_FUNCTIONS = {
    "find_customer_by_email": find_customer_by_email,
    "find_order": find_order,
    "get_refund_policy": get_refund_policy,
    "evaluate_refund": evaluate_refund,
}

SYSTEM_PROMPT = """
You are an AI Customer Support Agent for an e-commerce company.
You must call evaluate_refund before giving any final approval, denial, store-credit, or manual-review response.
You must never approve refunds from general knowledge.
You must use tools to inspect customer/order data and refund policy.
If policy denies a refund, politely hold the line.
Return a helpful customer-facing response.
"""


def run_agent(user_message: str):
    logs = []
    final_decision = None
    current_order_id = None

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message},
    ]

    for i in range(5):
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
        )

        assistant_message = response.choices[0].message
        messages.append(assistant_message)

        if assistant_message.tool_calls:
            for tool_call in assistant_message.tool_calls:
                tool_name = tool_call.function.name
                args = json.loads(tool_call.function.arguments or "{}")

                logs.append({
                    "step": f"Planning tool call: {tool_name}",
                    "detail": f"Agent selected `{tool_name}` with arguments: {json.dumps(args)}",
                })

                result = TOOL_FUNCTIONS[tool_name](**args)

                if tool_name == "find_order" and "error" not in result:
                    current_order_id = result.get("order_id")

                if tool_name == "evaluate_refund":
                    final_decision = result.get("decision")

                if tool_name == "get_refund_policy":
                    log_detail = (
                        "Refund policy loaded successfully. "
                        "The agent will validate the refund window, item category, "
                        "item condition, customer risk status, and customer tier."
                    )
                else:
                    log_detail = json.dumps(result, indent=2)

                logs.append({
                    "step": f"Tool result received: {tool_name}",
                    "detail": log_detail,
                })

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result),
                })

        else:
            if final_decision is None and current_order_id:
                evaluation_result = evaluate_refund(current_order_id)
                final_decision = evaluation_result.get("decision")

                logs.append({
                    "step": "Required policy evaluation",
                    "detail": (
                        f"The agent had not called evaluate_refund, so the backend "
                        f"enforced deterministic policy validation for "
                        f"order {current_order_id}."
                    ),
                })

                logs.append({
                    "step": "Tool result received: evaluate_refund",
                    "detail": json.dumps(evaluation_result, indent=2),
                })

                messages.append({
                    "role": "user",
                    "content": (
                        "A required deterministic refund evaluation has now been "
                        f"completed with this result: {json.dumps(evaluation_result)}. "
                        "Provide the final customer-facing response. Follow the "
                        "decision exactly and do not call additional tools."
                    ),
                })

                continue

            return {
                "answer": assistant_message.content,
                "decision": final_decision,
                "logs": logs,
            }

    return {
        "answer": "I’m sorry, I could not complete the refund review. I’ll route this to a human support specialist.",
        "decision": "manual_review",
        "logs": logs,
    }