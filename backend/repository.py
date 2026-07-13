from sqlalchemy import select

from database import SessionLocal
from models import Customer, Order


def customer_to_dict(customer: Customer) -> dict:
    return {
        "customer_id": customer.customer_id,
        "name": customer.name,
        "email": customer.email,
        "tier": customer.tier,
        "total_orders": customer.total_orders,
        "risk_flag": customer.risk_flag,
    }


def order_to_dict(order: Order) -> dict:
    return {
        "order_id": order.order_id,
        "customer_id": order.customer_id,
        "item": order.item,
        "amount": order.amount,
        "days_since_delivery": order.days_since_delivery,
        "condition": order.condition,
        "category": order.category,
    }


def find_customer_by_email(email: str) -> dict:
    with SessionLocal() as session:
        statement = select(Customer).where(
            Customer.email == email.lower()
        )

        customer = session.scalar(statement)

        if customer is None:
            return {"error": "Customer not found"}

        return customer_to_dict(customer)


def find_order(order_id: str) -> dict:
    with SessionLocal() as session:
        statement = select(Order).where(
            Order.order_id == order_id.upper()
        )

        order = session.scalar(statement)

        if order is None:
            return {"error": "Order not found"}

        return order_to_dict(order)


def find_customer_by_id(customer_id: str) -> dict:
    with SessionLocal() as session:
        statement = select(Customer).where(
            Customer.customer_id == customer_id
        )

        customer = session.scalar(statement)

        if customer is None:
            return {"error": "Customer not found"}

        return customer_to_dict(customer)


def get_all_customers() -> list[dict]:
    with SessionLocal() as session:
        customers = session.scalars(select(Customer)).all()

        return [
            customer_to_dict(customer)
            for customer in customers
        ]


def get_all_orders() -> list[dict]:
    with SessionLocal() as session:
        orders = session.scalars(select(Order)).all()

        return [
            order_to_dict(order)
            for order in orders
        ]