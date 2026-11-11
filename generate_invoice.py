import sqlite3

def generate_invoice(order_id):
    connection = sqlite3.connect("tienda_virtual.db")
    cursor = connection.cursor()

    #1. Query to get customer and order header information
    try:
        cursor.execute("""
            SELECT u.name, o.status
            FROM "Order" o
            JOIN User u ON o.user_id = u.user_id
            where o.order_id = ?
        """, (order_id,))
        
        order_data = cursor.fetchone()
        
        if not order_data:
            print("\n[!] Order not found. ")
            connection.close()
            return
        
        customer_name, order_status = order_data

        # 2. Query to get the products linked to this order
        # I also used JOIN between Order_items and Product

        cursor.execute("""
            SELECT p.name, oi.quantity, p.price, (oi.quantity * p.price) as subtotal
            FROM Order_items oi
            JOIN Product p ON oi.product_id = p.product_id
            WHERE oi.order_id = ?
            """, (order_id,))
        
        items = cursor.fetchall()

        if not items:
            print(f"\n[!] Order #{order_id} exists but has no products linked yet.")
            connection.close()
            return
        
        # 3. Visual design of the invoice 
        line_width = 50
        print("\n" + "="* line_width)
        invoice_title = f"INVOICE FOR ORDER #{order_id}"
        print(f"{invoice_title:^{line_width}}")
        print("="*line_width)
        print(f"Customer: {customer_name.upper()}")
        print(f"Status: {order_status.capitalize()}")
        print("-"*line_width)

        # headers with columns with professional alignment
        print(f"{'Product':<20} {'Qty':>5} {'Price':>10} {'Subtotal':>12}")
        print("-"*line_width)

        total_amount = 0
        for item in items:
            name, qty, price, subtotal = item
            total_amount += subtotal
            # Using the same aligment for the data 
            print(f"{name:<20} {qty:>5} {price:>10.2f} {subtotal:>12.2f}")

        # The invoice footer
        print("-"*line_width)
        total_label = "TOTAL AMOUNT:"
        # Aligning the total amount to the left and the value to the right
        print(f"{total_label:<30} {'$':>5}{total_amount:>11.2f}")
        print("="*line_width)

        thanks_msg = 'Thank you for your purchase!'
        print(f"{thanks_msg:^{line_width}}")
        print("="*line_width)
        
    except Exception as e:
        print(f"\n[!] A database error occurred: {e}")

    finally:
        connection.close()

if __name__ == "__main__":
    val = input(" Enter Order ID to generate invoice: ")
    if val.isdigit():
        generate_invoice(val)
    else:
        print("\n[!] Invalid input. Please enter a number")


    


            
