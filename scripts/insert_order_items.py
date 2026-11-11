import sqlite3
 
def add_items_to_order():
    connection = sqlite3.connect("tienda_virtual.db")
    cursor = connection.cursor()

    print("///////// Add Items to Order /////////")

    # 1. loop until a valid order ID is provided
    while True:
        order_id_str = input("Enter the Order ID: ").strip()
        if not order_id_str:
            print("Order ID cannot be empty. Please try again.")
            continue

        try:
            order_id = int(order_id_str)
        except ValueError:
            print("[!] Error: Order ID must be a number. Please try again.")
            continue

        # FIX 1: Added "status" to the SELECT statement so index [1] works safely!
        cursor.execute('SELECT order_id, status FROM "Order" WHERE order_id = ?', (order_id,))
        order_exists = cursor.fetchone()

        if not order_exists:
            print(f"[!] Error: Order ID {order_id} does not exist. Please try again.")
            continue

        # Business rules bonus: don't add items to completed or cancelled orders
        # Using .capitalize() helps match "Pending", "Completed", or "Cancelled" structures
        if order_exists[1].capitalize() in ['Completed', 'Cancelled']:
            print(f"[!] Error: Order #{order_id} is already '{order_exists[1]}'. You cannot add items to it.")
            connection.close()
            return
        
        break # Exit the loop if a valid order ID is provided


    # 2. loop until a valid product ID is provided
    while True:
        product_id_str = input("Enter the product ID to add: ").strip()

        if not product_id_str:
            print("[!] Error: Product ID cannot be empty. Please try again.")
            continue

        try:
            product_id = int(product_id_str)
        except ValueError:
            print("[!] Error: Product ID must be a number. Please try again.")
            continue

        # FIX 2: Added "price" to the SELECT statement so index [2] works safely!
        cursor.execute('SELECT name, stock, price FROM Product WHERE product_id = ?', (product_id,))
        product_exists = cursor.fetchone()

        if not product_exists:
            print(f"[!] Error: Product ID  #{product_id} does not exist. Please try again.")
            continue

        product_name = product_exists[0]
        product_stock = product_exists[1]
        product_price = product_exists[2]

        break # Exit the loop

    # 3. Loop until a valid quantity is provided 
    while True:
        quantity_str = input(f"Enter the quantity of '{product_name}' to add (Available Stock: {product_stock}): ").strip()
        if not quantity_str:
            print("[!] Error: Quantity cannot be empty. Please try again.")
            continue
        try:
            quantity = int(quantity_str)
            if quantity <= 0:
                print("[!] Error: Quantity must be a positive number greater than zero. Please try again.")
                continue
            
            # FIX 3: Added missing stock protection check!
            if quantity > product_stock:
                print(f"[!] Error: Insufficient stock. Only {product_stock} available. Please try again.")
                continue

        except ValueError:
            print("[!] Error: Quantity must be a number. Please try again.")
            continue
        
        break # Exit the loop if valid quantity is provided

    # 4. save database transaction execution
    try: 
        # FIX 4: Ensured table name matches standard snake_case "Order_items"
        cursor.execute('''
            INSERT INTO Order_items (order_id, product_id, quantity) 
            VALUES (?, ?, ?)
        ''', (order_id, product_id, quantity))
        
        # 2. Update product stock
        cursor.execute('''
            UPDATE Product
            SET stock = stock - ?
            WHERE product_id = ?
        ''', (quantity, product_id))

        # commit both operations together
        connection.commit()

        total_cost = quantity * product_price
        print(f"\n[SUCCESS] Added {quantity} of '{product_name}' to Order #{order_id}.")
        print(f"Inventory Deducted: -{quantity} units | Transaction Value: ${total_cost:,.2f}")
    
    except Exception as e:
        connection.rollback() # Undo changes if anything crashes mid-way
        print(f"\n[!] Database Transaction Error: {e}")

    finally:
        connection.close()

if __name__ == "__main__":
    add_items_to_order()