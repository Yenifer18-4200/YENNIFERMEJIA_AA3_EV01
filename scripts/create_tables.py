import sqlite3

def create_tables():
    # Create the connection and the database file
    connection = sqlite3.connect("tienda_virtual.db")
    cursor = connection.cursor()

    # Create User Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS User (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(150) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        role VARCHAR(20) NOT NULL
    )
    ''')

    # Create Product Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Product (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(100) NOT NULL,
        price DECIMAL(10,2) NOT NULL,
        stock INTEGER NOT NULL
    )
    ''')

    # Create Order Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS "Order" (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        total_amount DECIMAL(10,2) NOT NULL,
        status VARCHAR(20) NOT NULL,
        date TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES User (user_id)
    )
    ''')
    
    # Create Order Items Table 
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Order_items (
        order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        FOREIGN KEY (order_id) REFERENCES "Order" (order_id),
        FOREIGN KEY (product_id) REFERENCES Product (product_id)
    )
    ''')

    connection.commit()
    print("¡Database and tables successfully created following the ERD!")
    connection.close()

if __name__ == "__main__":
    create_tables()