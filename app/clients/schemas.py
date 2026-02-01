from pydantic import BaseModel
from typing import List, Optional
from datetime import date


class Movement(BaseModel):
    id: int
    occurredAt: date
    amountCents: int
    type: str
    categoryId: Optional[int] = None
    description: Optional[str] = None


class PaginatedMovements(BaseModel):
    items: List[Movement]
    page: int
    pageSize: int
    total: int


class TotalAmount(BaseModel):
    totalCents: int


class CategoryTotal(BaseModel):
    categoryId: int
    totalCents: int


class ExpensesByCategory(BaseModel):
    items: List[CategoryTotal]
