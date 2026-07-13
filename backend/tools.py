from data import CUSTOMERS, ORDERS
from policy import REFUND_POLICY


def find_customer_by_email(email: str):
    for customer in CUSTOMERS:
        if customer["email"].lower() == email.lower():
            return customer
    return {"error": "Customer not found"}


def find_order(order_id: str):
    for order in ORDERS:
        if order["order_id"].lower() == order_id.lower():
            return order
    return {"error": "Order not found"}


def get_refund_policy():
    return REFUND_POLICY


def evaluate_refund(order_id: str):
    order = find_order(order_id)

    if "error" in order:
        return {"decision": "deny", "reason": "Order not found"}

    customer = next((c for c in CUSTOMERS if c["customer_id"] == order["customer_id"]), None)

    if customer and customer["risk_flag"]:
        return {"decision": "manual_review", "reason": "Customer account has a risk flag"}

    if order["category"] == "final_sale":
        return {"decision": "deny", "reason": "Final sale items are not refundable"}

    if order["days_since_delivery"] > 30:
        return {"decision": "deny", "reason": "Refund window exceeded"}

    if order["condition"] == "damaged_by_customer":
        return {"decision": "deny", "reason": "Customer-damaged items are not refundable"}

    if order["condition"] == "lightly_used" and order["category"] == "apparel":
        return {"decision": "store_credit", "reason": "Lightly used apparel qualifies for store credit only"}

    if order["condition"] in ["unopened", "defective"]:
        return {"decision": "approve", "reason": "Item meets refund policy requirements"}

    return {"decision": "manual_review", "reason": "Unable to determine refund eligibility"}