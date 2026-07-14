from prometheus_client import Counter, Histogram


HTTP_REQUESTS_TOTAL = Counter(
    "smartshop_http_requests_total",
    "Total number of HTTP requests.",
    ["method", "path", "status_code"],
)

HTTP_REQUEST_DURATION_SECONDS = Histogram(
    "smartshop_http_request_duration_seconds",
    "HTTP request duration in seconds.",
    ["method", "path"],
)

CHAT_REQUESTS_TOTAL = Counter(
    "smartshop_chat_requests_total",
    "Total number of chat requests.",
    ["status"],
)

REFUND_DECISIONS_TOTAL = Counter(
    "smartshop_refund_decisions_total",
    "Total refund decisions produced by the agent.",
    ["decision"],
)

AGENT_EXECUTION_DURATION_SECONDS = Histogram(
    "smartshop_agent_execution_duration_seconds",
    "Total LangGraph agent execution duration in seconds.",
)

LLM_CALLS_TOTAL = Counter(
    "smartshop_llm_calls_total",
    "Total number of LLM calls.",
)

LLM_ERRORS_TOTAL = Counter(
    "smartshop_llm_errors_total",
    "Total number of failed LLM calls.",
)

AGENT_TOOL_CALLS_TOTAL = Counter(
    "smartshop_agent_tool_calls_total",
    "Total number of agent tool calls.",
    ["tool"],
)

AGENT_TOOL_ERRORS_TOTAL = Counter(
    "smartshop_agent_tool_errors_total",
    "Total number of failed agent tool calls.",
    ["tool"],
)

POLICY_ENFORCEMENTS_TOTAL = Counter(
    "smartshop_policy_enforcements_total",
    "Number of times deterministic policy evaluation was enforced.",
)