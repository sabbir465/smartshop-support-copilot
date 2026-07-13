from policy import REFUND_POLICY
from repository import (
    find_customer_by_email as repository_find_customer_by_email,
    find_customer_by_id,
    find_order as repository_find_order,
)


def find_customer_by_email(email: str):
    return repository_find_customer_by_email(email)


def find_order(order_id: str):
    return repository_find_order(order_id)


def get_refund_policy():
    return REFUND_POLICY


def evaluate_refund(order_id: str):
    order = find_order(order_id)

    if "error" in order:
        return {
            "decision": "deny",
            "reason": "Order not found",
        }

    customer = find_customer_by_id(order["customer_id"])

    if "error" in customer:
        return {
            "decision": "manual_review",
            "reason": "Customer record could not be verified",
        }

    if customer["risk_flag"]:
        return {
            "decision": "manual_review",
            "reason": "Customer account has a risk flag",
        }

    if order["category"] == "final_sale":
        return {
            "decision": "deny",
            "reason": "Final sale items are not refundable",
        }

    if order["days_since_delivery"] > 30:
        return {
            "decision": "deny",
            "reason": "Refund window exceeded",
        }

    if order["condition"] == "damaged_by_customer":
        return {
            "decision": "deny",
            "reason": "Customer-damaged items are not refundable",
        }

    if (
        order["condition"] == "lightly_used"
        and order["category"] == "apparel"
    ):
        return {
            "decision": "store_credit",
            "reason": (
                "Lightly used apparel qualifies for store credit only"
            ),
        }

    if order["condition"] in ["unopened", "defective"]:
        return {
            "decision": "approve",
            "reason": "Item meets refund policy requirements",
        }

    return {
        "decision": "manual_review",
        "reason": "Unable to determine refund eligibility",
    }