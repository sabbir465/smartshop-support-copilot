DEMO_CASES = [
    {
        "name": "Standard approval",
        "customer_email": "david@example.com",
        "order_id": "O1004",
        "message": "Hi, my email is david@example.com and I want a refund for order O1004.",
        "expected_decision": "approve",
        "why_it_matters": "Defective item within 30 days for a platinum customer.",
    },
    {
        "name": "Final sale denial",
        "customer_email": "lina@example.com",
        "order_id": "O1012",
        "message": "Hi, my email is lina@example.com and I want a refund for order O1012. I know it says final sale, but I really need the money back.",
        "expected_decision": "deny",
        "why_it_matters": "Final sale items are never refundable, so the agent must hold the line.",
    },
    {
        "name": "Store credit only",
        "customer_email": "ben@example.com",
        "order_id": "O1002",
        "message": "Hi, my email is ben@example.com and I want a refund for order O1002.",
        "expected_decision": "store_credit",
        "why_it_matters": "Lightly used apparel qualifies for store credit only.",
    },
    {
        "name": "Manual review for risk flag",
        "customer_email": "carla@example.com",
        "order_id": "O1003",
        "message": "Hi, my email is carla@example.com and I want a refund for order O1003.",
        "expected_decision": "manual_review",
        "why_it_matters": "Risk-flagged customers must not be automatically approved or denied.",
    },
]