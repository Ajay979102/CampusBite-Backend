from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.menu import MenuCreate, MenuUpdate
from app.services.menu_service import (
    create_menu_item,
    get_all_menu_items,
    get_menu_item,
    update_menu_item,
    delete_menu_item
)

router = APIRouter(
    prefix="/menu",
    tags=["Menu"]
)


# Add Menu Item
@router.post("/")
def add_menu(
    data: MenuCreate,
    db: Session = Depends(get_db)
):
    return create_menu_item(db, data)


# Get All Menu Items
@router.get("/")
def get_menu(
    db: Session = Depends(get_db)
):
    return get_all_menu_items(db)


# Get Single Menu Item
@router.get("/{menu_id}")
def get_single_menu(
    menu_id: int,
    db: Session = Depends(get_db)
):
    return get_menu_item(db, menu_id)


# Update Menu Item
@router.put("/{menu_id}")
def update_menu(
    menu_id: int,
    data: MenuUpdate,
    db: Session = Depends(get_db)
):
    return update_menu_item(
        db,
        menu_id,
        data
    )


# Delete Menu Item
@router.delete("/{menu_id}")
def delete_menu(
    menu_id: int,
    db: Session = Depends(get_db)
):
    return delete_menu_item(
        db,
        menu_id
    )