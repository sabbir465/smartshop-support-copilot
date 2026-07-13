from tools import evaluate_refund


def test_approve_defective_item_within_window():
    result = evaluate_refund("O1004")

    assert result["decision"] == "approve"
    assert result["reason"] == "Item meets refund policy requirements"


def test_deny_final_sale_item():
    result = evaluate_refund("O1012")

    assert result["decision"] == "deny"
    assert result["reason"] == "Final sale items are not refundable"


def test_deny_order_outside_refund_window():
    result = evaluate_refund("O1006")

    assert result["decision"] == "deny"
    assert result["reason"] == "Refund window exceeded"


def test_manual_review_for_risk_flag():
    result = evaluate_refund("O1010")

    assert result["decision"] == "manual_review"
    assert result["reason"] == "Customer account has a risk flag"


def test_store_credit_for_lightly_used_apparel():
    result = evaluate_refund("O1002")

    assert result["decision"] == "store_credit"
    assert (
        result["reason"]
        == "Lightly used apparel qualifies for store credit only"
    )


def test_deny_unknown_order():
    result = evaluate_refund("O9999")

    assert result["decision"] == "deny"
    assert result["reason"] == "Order not found"