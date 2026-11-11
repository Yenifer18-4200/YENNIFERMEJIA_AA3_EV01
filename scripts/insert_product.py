
import sqlite3

def register_product():
    # Brigde to the database
    connection = sqlite3.connect("tienda_virtual.db")
    cursor = connection.cursor()

    print("///////// Product Registration //////////")
    
    while True:
        # 1. capture inputs cleanly as strings first
        name_str = input("Enter the product name: ").strip()           
        price_str = input("Enter the product price: ").strip()
        stock_str = input("Enter the initial stock quantity: ").strip()

        # 2. VALIDATION: Check for empty fields
        if not name_str or not price_str or not stock_str:
         print("\n[!] Registration failed: All fields are mandatory. Please try again.")
         continue

        # 3. type conversion and rules validation inside the try block
        try: 
            price = float(price_str)
            stock = int(stock_str)

        #  Rules checks
            if price <= 0:
                print("\n[!] Registration failed: Price must be a positive number greater than zero. Please enter a valid price.")
                continue

            if stock < 0:
                print("\n[!] Registration failed: Stock quantity cannot be negative. Please enter a valid stock quantity.")
                continue

        except ValueError:
            print("\n[!] Invalid input: Price must be a number and stock must be an integer. Please enter valid data.")
            continue

        # 4. Database execution: 

        try:
           #SQL command  to insert the data into the products table
           cursor.execute('''
                INSERT INTO Product (name, price, stock)
                VALUES (?, ?, ?)
            ''', (name_str, price, stock))
        
           connection.commit()
           print(f"\nSuccessfully registered the product: '{name_str}' has been added to the catalog.")
           break # Exit the loop after successful registration
    
        except sqlite3.IntegrityError:
              print(f"\n[!] Error: A product named '{name_str}' already exists in the database. Please choose a different name.")
              continue
        
        except Exception as e:
           print(f"\nAn error occurred: {e}")
           break

        
    connection.close()

if __name__ == "__main__":
    register_product()


        
        




