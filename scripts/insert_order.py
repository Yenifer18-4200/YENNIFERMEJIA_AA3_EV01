import sqlite3
from datetime import datetime

def create_order():
    # Bridge to the database
    connection = sqlite3.connect("tienda_virtual.db")
    cursor = connection.cursor()

    print("///////// Create Order /////////")

    # 1. loop until a valid user ID is provided
    while True:
        user_id_str = input("Enter the user ID: ").strip()
        if not user_id_str:
            print("[!] Error: User ID cannot be empty. Please try again.")
            continue

        try:
            user_id = int(user_id_str)
        except ValueError:
            print("[!] Error: User ID must be a whole number. Please try again.")
            continue

        cursor.execute("SELECT name FROM User WHERE user_id = ?", (user_id,))
        user_exists = cursor.fetchone()

        if not user_exists:
            print(f"[!] Error: User with ID {user_id} does not exist. ")
            continue

        if user_exists[0] == "":
            print(f"[!] Error: User ID {user_id} contains an empty profile name. ")
            continue

        customer_name = user_exists[0]
        break # exit the loop if a valid user ID is provided

    # 2. Loop until a valid Total Amount is provided
    while True:
        total_amount_str = input("Enter the total amount: ").strip()
        if not total_amount_str:
            print("[!] Error: Total amount cannot be empty. Please try again.")
            continue

        try:

            total_amount = float(total_amount_str)

            if total_amount < 0:
                print("[!] Error: Total amount cannot be negative. Please try again.")
                continue

            break #exit amount loop
        except ValueError:
            print("[!] Error: Total amount must be a numeric value. Please try again.")

    # 3. Loop until a valid status is provided
    while True:
        status = input("Enter the order status (Pending/Completed/Cancelled): ").strip().capitalize()
        if not status:
            print("[!] Error: Status cannot be empty. Please try again.")
            continue

        if status not in ["Pending", "Completed", "Cancelled"]:
            print("[!] Error: Invalid status. Please enter Pending, Completed, or Cancelled.")
            continue

        break # exit status loop

    # 4. AUTOMATE THE DATE
    # Generate a clean timestamp: YYYY-MM-DD HH:MM:SS
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 5. Safe database execution
    try:
        cursor.execute('''
            INSERT INTO "Order" (user_id, total_amount, status, date)
            VALUES (?, ?, ?, ?)
        ''', (user_id, total_amount, status, current_date))

        connection.commit()

        order_id = cursor.lastrowid
        print(f"\n[SUCCESS] Order #{order_id} successfully created for customer '{customer_name}'!")
        print(f"Date: {current_date} | Total Amount: ${total_amount:,.2f} | Status: {status}")

    except Exception as e:
        print(f"[!] Database error: {e}")

    connection.close()

if __name__ == "__main__":
    create_order()
