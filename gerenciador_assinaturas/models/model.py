from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import date
from decimal import Decimal

class Subscription(SQLModel, table=True):
    ID: int = Field(primary_key=True)
    company: str
    site: Optional[str] = None
    sub_date: date
    value: Decimal

class Payment(SQLModel, table=True):
    ID: int = Field(primary_key=True)
    subscription_id: int = Field(foreign_key='subscription.ID')
    subscription: Subscription = Relationship()
    date: date 