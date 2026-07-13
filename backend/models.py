from sqlalchemy import Boolean, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    customer_id: Mapped[str] = mapped_column(
        String,
        unique=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(String)

    email: Mapped[str] = mapped_column(
        String,
        unique=True,
        index=True,
    )

    tier: Mapped[str] = mapped_column(String)

    total_orders: Mapped[int] = mapped_column(Integer)

    risk_flag: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    orders: Mapped[list["Order"]] = relationship(
        back_populates="customer",
    )


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    order_id: Mapped[str] = mapped_column(
        String,
        unique=True,
        index=True,
    )

    customer_id: Mapped[str] = mapped_column(
        ForeignKey("customers.customer_id"),
        index=True,
    )

    item: Mapped[str] = mapped_column(String)

    amount: Mapped[float] = mapped_column(Float)

    days_since_delivery: Mapped[int] = mapped_column(Integer)

    condition: Mapped[str] = mapped_column(String)

    category: Mapped[str] = mapped_column(String)

    customer: Mapped[Customer] = relationship(
        back_populates="orders",
    )