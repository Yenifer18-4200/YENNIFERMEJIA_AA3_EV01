import sqlite3

def show_inventory():
    connection = sqlite3.connect("tienda_virtual.db")
    cursor = connection.cursor()

    print("\n" + "-"*15 + " REGISTERED USERS " + "-"*15)
    try:
        # * Bring all the columns without mattering its name
        cursor.execute("SELECT * FROM User")
        users = cursor.fetchall()

        if not users: # If the list is empty, it means  there are no users registered
            print("No users registered yet.")

        for u in users:
            # print for seeing what is inside
            print(f"ID: {u[0]:<4} | Name: {u[1]:<12} | Email: {u[2]:<15} | Password: {u[3]:<10} | Role: {u[4]:<10}")

    except Exception as e:
        print(f"Error in user table: {e}")


    print("\n" + "-"*15 + " REGISTERED PRODUCTS " + "-"*15)
    try:
        cursor.execute("SELECT product_id, name, price, stock FROM Product")
        products = cursor.fetchall()
        
        if not products:
            print("No products registered yet.")

        for p in products:
            print(f"ID: {p[0]:<4} | name: {p[1]:<20} | Price: ${p[2]:,.2f} | Stock: {p[3]:<6}")
            
    except Exception as e:
        print(f"Error in product table: {e}")
    connection.close()

if  __name__ == "__main__":
    show_inventory()
