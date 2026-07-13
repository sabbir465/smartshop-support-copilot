from database import Base, SessionLocal, engine
from data import CUSTOMERS, ORDERS
from models import Customer, Order


def seed_database() -> None:
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as session:
        existing_customer = session.query(Customer).first()

        if existing_customer:
            print("Database already contains seed data.")
            return

        customers = [
            Customer(
                customer_id=customer["customer_id"],
                name=customer["name"],
                email=customer["email"],
                tier=customer["tier"],
                total_orders=customer["total_orders"],
                risk_flag=customer["risk_flag"],
            )
            for customer in CUSTOMERS
        ]

        session.add_all(customers)
        session.flush()

        orders = [
            Order(
                order_id=order["order_id"],
                customer_id=order["customer_id"],
                item=order["item"],
                amount=order["amount"],
                days_since_delivery=order["days_since_delivery"],
                condition=order["condition"],
                category=order["category"],
            )
            for order in ORDERS
        ]

        session.add_all(orders)
        session.commit()

        print(
            f"Seeded {len(customers)} customers "
            f"and {len(orders)} orders successfully."
        )


if __name__ == "__main__":
    seed_database()