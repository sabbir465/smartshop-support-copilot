REFUND_POLICY = """
SmartShop Refund Policy v1.0

1. Refund Window
- Refunds are only allowed within 30 calendar days of delivery.
- Requests after 30 days must be denied unless escalated by a human manager.

2. Final Sale Items
- Items in the final_sale category are never refundable.
- Agents must politely hold the line even if the customer asks for an exception.

3. Item Condition
- Unopened items are eligible for refund within 30 days.
- Defective items are eligible for refund within 30 days.
- Customer-damaged items are not refundable.
- Opened items require manual review unless marked defective.
- Lightly used apparel is eligible for store credit only, not cash refund.

4. Customer Risk
- Customers with risk_flag=True must be routed to manual review.
- The agent must not approve or deny high-risk customers automatically.

5. Customer Tier
- Platinum customers may receive expedited processing only if the refund is otherwise policy-compliant.
- Customer tier cannot override final_sale, risk_flag, customer damage, or refund window rules.

6. Required Agent Behavior
- The agent must use customer data, order data, and policy rules before making a decision.
- The agent must explain the decision clearly and politely.
- The agent must not invent exceptions.
- When denying a refund, the agent should acknowledge the customer’s concern but enforce the policy.
"""