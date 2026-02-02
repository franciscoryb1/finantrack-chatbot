from typing import List, Optional
from pydantic import BaseModel, Field


# =========================
# MODELOS BASE
# =========================

class Movement(BaseModel):
    id: int
    date: str
    description: str
    amount: float
    type: str  # income | expense
    category_id: Optional[int] = None
    category_name: Optional[str] = None
    account_id: Optional[int] = None
    account_name: Optional[str] = None


# =========================
# RESPUESTAS PAGINADAS
# =========================

class Pagination(BaseModel):
    page: int
    page_size: int = Field(alias="pageSize")
    total_items: int = Field(alias="totalItems")
    total_pages: int = Field(alias="totalPages")


class PaginatedMovements(BaseModel):
    items: List[Movement]
    pagination: Pagination


# =========================
# TOTALES
# =========================

class TotalAmount(BaseModel):
    total: float


class CategoryAmount(BaseModel):
    category_id: int
    category_name: str
    total: float


class ExpensesByCategory(BaseModel):
    items: List[CategoryAmount]
