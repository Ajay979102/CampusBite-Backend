from pydantic import BaseModel


class MenuCreate(BaseModel):
    item_name: str
    category: str
    price: float
    available: bool = True


class MenuUpdate(BaseModel):
    item_name: str
    category: str
    price: float
    available: bool


class MenuResponse(BaseModel):
    id: int
    item_name: str
    category: str
    price: float
    available: bool

    class Config:
        from_attributes = True