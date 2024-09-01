from sqlalchemy import Enum
from enum import Enum as PyEnum

class OrderType(PyEnum):
    BUY = "buy"
    SELL = "sell"

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    coin = Column(String)
    amount = Column(Float)
    price = Column(Float)
    order_type = Column(Enum(OrderType))
    status = Column(String, default="pending")

def create_order(user_id, coin, amount, price, order_type):
    order = Order(user_id=user_id, coin=coin, amount=amount, price=price, order_type=order_type)
    session.add(order)
    session.commit()
    return order

def get_orders():
    return session.query(Order).all()