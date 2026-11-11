import sqlite3
from fastapi import APIRouter, HTTPException
from app.schemas import ProductCreate, ProductUpdate

# Create router instance with prefix and tags for Swagger UI grouping
router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

# --- READ ENDPOINTS ---

@router.get("")
def get_products():
    conn = sqlite3.connect("tienda_virtual.db")
    cursor = conn.cursor()
    cursor.execute("SELECT product_id, name, price, stock FROM Product")
    rows = cursor.fetchall()
    conn.close()
    
    products = []
    for row in rows:
        products.append({
            "product_id": row[0],  
            "name": row[1],
            "price": row[2],
            "stock": row[3]
        })
    return {"products": products}

@router.get("/{product_id}")
def get_single_product(product_id: int):
    conn = sqlite3.connect("tienda_virtual.db")
    cursor = conn.cursor()
    cursor.execute("SELECT product_id, name, price, stock FROM Product WHERE product_id = ?", (product_id,))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found")
        
    return {
        "product_id": row[0],
        "name": row[1],
        "price": row[2],
        "stock": row[3]
    }

# --- WRITE ENDPOINTS (Admin Tools) ---

@router.post("")
def create_product(product: ProductCreate):
    conn = sqlite3.connect("tienda_virtual.db")
    cursor = conn.cursor()

    # Check if a product with the same name already exists (case-insensitive check)
    cursor.execute("SELECT product_id FROM Product WHERE name = ?", (product.name.lower(),))
    existing_product = cursor.fetchone()
    if existing_product:
        conn.close()
        raise HTTPException(status_code=400, detail=f"Product with name '{product.name}' already exists.")
    
    # Insert new product
    cursor.execute(
        "INSERT INTO Product (name, price, stock) VALUES (?, ?, ?)",
        (product.name.lower(), product.price, product.stock)
    )

    new_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return {
        "message": "Product created successfully! 📦", 
        "product_id": new_id, 
        "name": product.name.lower(), 
        "price": product.price, 
        "stock": product.stock
    }

@router.put("/{product_id}")
def update_product(product_id: int, product_update: ProductUpdate):
    conn = sqlite3.connect("tienda_virtual.db")
    cursor = conn.cursor()

    # Verify that the product exists and fetch current values
    cursor.execute("SELECT name, price, stock FROM Product WHERE product_id = ?", (product_id,))
    existing_product = cursor.fetchone()
    if not existing_product:
        conn.close()
        raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found")
    
    current_name, current_price, current_stock = existing_product

    # Only update values that are explicitly provided in the request body
    new_price = product_update.price if product_update.price is not None else current_price
    new_stock = product_update.stock if product_update.stock is not None else current_stock

    # Execute safe database update
    cursor.execute(
        "UPDATE Product SET price = ?, stock = ? WHERE product_id = ?",
        (new_price, new_stock, product_id)
    )

    conn.commit()
    conn.close()

    return {
        "message": "Product updated successfully 🔄", 
        "product_id": product_id,
        "new_price": new_price,
        "new_stock": new_stock
    }

@router.delete("/{product_id}")
def delete_product(product_id: int):
    conn = sqlite3.connect("tienda_virtual.db")
    cursor = conn.cursor()

    # Verify that the product exists
    cursor.execute("SELECT product_id FROM Product WHERE product_id = ?", (product_id,))
    existing_product = cursor.fetchone()
    if not existing_product:
        conn.close()
        raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found")

    # Delete the product
    cursor.execute("DELETE FROM Product WHERE product_id = ?", (product_id,))
    conn.commit()
    conn.close()

    return {
        "message": "Product deleted successfully 🗑️",
        "product_id": product_id
    }