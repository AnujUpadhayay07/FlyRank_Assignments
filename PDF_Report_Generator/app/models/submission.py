from sqlalchemy import Column, Integer, String, Float
from app.db.database import Base


class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String)
    product = Column(String)
    amount = Column(Float)
    status = Column(String)