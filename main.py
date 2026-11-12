from scripts.insert_product import register_product
import os
from generate_invoice import generate_invoice
from scripts.insert_order import create_order
from scripts.insert_order_items import add_items_to_order
from scripts.insert_user import register_user
from inventory_view import show_inventory
import sqlite3

# 1. Establish the connection to the SQLite database
connection = sqlite3.connect("virtual_store.db")
cursor = connection.cursor()

# 2. Add the tables creation logic
def init_db():
    # 1. User Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS User (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        email TEXT,
        password TEXT NOT NULL, 
        role TEXT NOT NULL      
    )''')

    # 2. Product Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Product (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        price REAL NOT NULL,
        stock INTEGER NOT NULL
    )''')

    # 3. Order Table (FIXED: Added missing 'date' column)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS "Order" (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        total_amount REAL,
        status TEXT,
        date TEXT, -- Added to match  insert_order implementation!
        FOREIGN KEY (user_id) REFERENCES User (user_id)
    )''')

    # 4. Order Items Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Order_items (
        order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        FOREIGN KEY (order_id) REFERENCES "Order" (order_id),
        FOREIGN KEY (product_id) REFERENCES Product (product_id)
    )''')
    
    connection.commit()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    while True:
        clear_screen()

        print("\n" + "=" * 45)
        print("     VIRTUAL STORE: ORDER MANAGEMENT")
        print("=" * 45)
        print("1. Register User")
        print("2. Register Product")
        print("3. View Inventory (users and products)")
        print("4. Create a new order")
        print("5. Add products to an order")
        print("6. Generate an invoice")
        print("7. Exit")
        print("=" * 45)

        try:
            user_input = input("Please select an option between(1-7): ")

            if not user_input.strip():
                continue

            option = int(user_input)

            if option == 1:
                print("\n[SYSTEM] Registering a new user...")
                register_user()

            elif option == 2:
                print("\n[SYSTEM] Adding a new product to the inventory...")
                register_product()

            elif option == 3:
                show_inventory()

            elif option == 4:
                print("\n[SYSTEM] Creating a new order...")
                create_order()

            elif option == 5:
                print("\n[SYSTEM] Adding products to an order...")
                add_items_to_order()

            elif option == 6:
                # Option 6 clean handoff to  verified standalone script logic
                order_id = input("\nEnter the order ID to generate the invoice: ")
                if order_id.isdigit():
                    generate_invoice(order_id)
                else: 
                    print("\n[!] Invalid order ID. Please enter a number.")

            elif option == 7:
                print("\nClosing the application. Goodbye!")
                connection.close() # FIXED: Safely disconnect global application stream
                break

            else:
                print(f"\n[!] Invalid option. Please try again.")

            input("\nPress enter to continue...")
                    
        except ValueError:
            print("\n[!] Invalid input. Please enter a number between 1 and 7.")
            input("\nPress enter to continue...")

if __name__ == "__main__":
    init_db()  # Triggers table validation/creation
    main()