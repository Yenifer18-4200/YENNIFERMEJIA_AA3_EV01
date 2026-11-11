from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
import sqlite3

# Import the schema we created in app/schemas.py
from app.schemas import OrderCreate  

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

@router.post("")
def create_order(order: OrderCreate):
    conn = sqlite3.connect("tienda_virtual.db")
    cursor = conn.cursor()
    
    # --- STEP 1: VALIDATE THE USER ---
    cursor.execute("SELECT name FROM User WHERE user_id = ?", (order.user_id,))
    user = cursor.fetchone()
    if user is None:
        conn.close()
        raise HTTPException(status_code=404, detail=f"User with ID {order.user_id} not found")
        
    # --- STEP 2: VALIDATE THE PRODUCT AND STOCK ---
    cursor.execute("SELECT name, price, stock FROM Product WHERE product_id = ?", (order.product_id,))
    product = cursor.fetchone()
    if product is None:
        conn.close()
        raise HTTPException(status_code=404, detail=f"Product with ID {order.product_id} not found")
        
    product_name, price, current_stock = product
    
    if current_stock < order.quantity:
        conn.close()
        raise HTTPException(status_code=400, detail=f"Not enough stock. Only {current_stock} available.")
        
    # --- STEP 3: CALCULATE TOTALS ---
    total_amount = price * order.quantity
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # --- STEP 4: INSERT INTO THE "Order" TABLE ---
    cursor.execute(
        'INSERT INTO "Order" (user_id, total_amount, status, date) VALUES (?, ?, ?, ?)', 
        (order.user_id, total_amount, "completed", current_date)
    )
    
    new_order_id = cursor.lastrowid
    
    # --- STEP 5: INSERT INTO Order_items TABLE ---
    cursor.execute(
        "INSERT INTO Order_items (order_id, product_id, quantity) VALUES (?, ?, ?)", 
        (new_order_id, order.product_id, order.quantity)
    )
    
    # --- STEP 6: UPDATE THE PRODUCT STOCK ---
    new_stock = current_stock - order.quantity
    cursor.execute(
        "UPDATE Product SET stock = ? WHERE product_id = ?", 
        (new_stock, order.product_id)
    )
    
    conn.commit()
    conn.close()
    
    return {
        "message": "Order processed successfully! 🎉",
        "order_id": new_order_id,
        "total_paid": total_amount,
        "remaining_stock": new_stock
    }

@router.get("")
def get_order_history():
    conn = sqlite3.connect("tienda_virtual.db")
    cursor = conn.cursor()

    cursor.execute('''SELECT order_id, user_id, date, total_amount FROM "Order" ORDER BY order_id DESC''')
    rows = cursor.fetchall()
    conn.close()

    orders = []
    for row in rows:
        orders.append({
            "order_id": row[0],
            "user_id": row[1],
            "date": row[2],
            "total_amount": row[3]
        })
    return {"orders": orders}