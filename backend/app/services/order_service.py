from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.menu import MenuItem


# =====================================
# Place Order
# =====================================
def place_order(
    db: Session,
    student_id: int,
    data
):
    try:
        total_amount = 0

        # Get Last Token Number
        last_order = (
            db.query(Order)
            .order_by(Order.id.desc())
            .first()
        )

        if last_order:
            token_number = last_order.token_number + 1
        else:
            token_number = 1

        # Create Order
        order = Order(
            student_id=student_id,
            total_amount=0,
            token_number=token_number,
            status="Pending"
        )

        db.add(order)
        db.commit()
        db.refresh(order)

        # Add Order Items
        for item in data.items:

            menu = (
                db.query(MenuItem)
                .filter(MenuItem.id == item.menu_item_id)
                .first()
            )

            # Menu Exists?
            if not menu:
                raise HTTPException(
                    status_code=404,
                    detail=f"Menu Item {item.menu_item_id} not found"
                )

            # Menu Available?
            if not menu.available:
                raise HTTPException(
                    status_code=400,
                    detail=f"{menu.item_name} is currently unavailable"
                )

            item_total = menu.price * item.quantity
            total_amount += item_total

            order_item = OrderItem(
                order_id=order.id,
                menu_item_id=menu.id,
                quantity=item.quantity,
                price=menu.price
            )

            db.add(order_item)

        # Update Total Amount
        order.total_amount = total_amount

        db.commit()
        db.refresh(order)

        return {
            "message": "Order Placed Successfully",
            "order_id": order.id,
            "token_number": order.token_number,
            "total_amount": order.total_amount,
            "status": order.status
        }

    except Exception:
        db.rollback()
        raise


# =====================================
# Get My Orders
# =====================================
def get_my_orders(
    db: Session,
    student_id: int
):
    orders = (
        db.query(Order)
        .filter(Order.student_id == student_id)
        .order_by(Order.id.desc())
        .all()
    )

    return orders


# =====================================
# Get Single Order
# =====================================
def get_single_order(
    db: Session,
    student_id: int,
    order_id: int
):
    order = (
        db.query(Order)
        .filter(
            Order.id == order_id,
            Order.student_id == student_id
        )
        .first()
    )

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    order_items = (
        db.query(OrderItem)
        .filter(OrderItem.order_id == order.id)
        .all()
    )

    items = []

    for item in order_items:

        menu = (
            db.query(MenuItem)
            .filter(MenuItem.id == item.menu_item_id)
            .first()
        )

        items.append(
            {
                "menu_item_id": menu.id,
                "item_name": menu.item_name,
                "quantity": item.quantity,
                "price": item.price,
                "subtotal": item.price * item.quantity
            }
        )

    return {
        "order_id": order.id,
        "token_number": order.token_number,
        "status": order.status,
        "total_amount": order.total_amount,
        "items": items
    }