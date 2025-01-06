from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date
from decimal import Decimal

class Subscription(SQLModel, table=True):
    ID: int = Field(primary_key=True)
    company: str
    site: Optional[str] = None
    sub_date: date
    value: Decimal