from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.menu import MenuItem


# -----------------------------
# Add Menu Item
# -----------------------------
def create_menu_item(db: Session, data):

    menu = MenuItem(
        item_name=data.item_name,
        category=data.category,
        price=data.price,
        available=data.available
    )

    db.add(menu)
    db.commit()
    db.refresh(menu)

    return {
        "message": "Menu Item Added Successfully",
        "menu": menu
    }


# -----------------------------
# Get All Menu Items
# -----------------------------
def get_all_menu_items(db: Session):

    menu = db.query(MenuItem).all()

    return menu


# -----------------------------
# Get Single Menu Item
# -----------------------------
def get_menu_item(db: Session, menu_id: int):

    menu = db.query(MenuItem).filter(
        MenuItem.id == menu_id
    ).first()

    if not menu:
        raise HTTPException(
            status_code=404,
            detail="Menu Item not found"
        )

    return menu


# -----------------------------
# Update Menu Item
# -----------------------------
def update_menu_item(
    db: Session,
    menu_id: int,
    data
):

    menu = db.query(MenuItem).filter(
        MenuItem.id == menu_id
    ).first()

    if not menu:
        raise HTTPException(
            status_code=404,
            detail="Menu Item not found"
        )

    menu.item_name = data.item_name
    menu.category = data.category
    menu.price = data.price
    menu.available = data.available

    db.commit()
    db.refresh(menu)

    return {
        "message": "Menu Updated Successfully",
        "menu": menu
    }


# -----------------------------
# Delete Menu Item
# -----------------------------
def delete_menu_item(
    db: Session,
    menu_id: int
):

    menu = db.query(MenuItem).filter(
        MenuItem.id == menu_id
    ).first()

    if not menu:
        raise HTTPException(
            status_code=404,
            detail="Menu Item not found"
        )

    db.delete(menu)
    db.commit()

    return {
        "message": "Menu Deleted Successfully"
    }