from typing import List

from pydantic import BaseModel, Field


# ==========================
# Order Item Request
# ==========================
class OrderItemRequest(BaseModel):
    menu_item_id: int
    quantity: int = Field(..., gt=0)


# ==========================
# Create Order Request
# ==========================
class OrderCreate(BaseModel):
    items: List[OrderItemRequest]


# ==========================
# Order Item Response
# ==========================
class OrderItemResponse(BaseModel):
    menu_item_id: int
    quantity: int
    price: float

    class Config:
        from_attributes = True


# ==========================
# Order Response
# ==========================
class OrderResponse(BaseModel):
    id: int
    student_id: int
    total_amount: float
    status: str
    token_number: int

    class Config:
        from_attributes = True