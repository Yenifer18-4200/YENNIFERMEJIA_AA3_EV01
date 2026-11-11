import sqlite3

def register_user():
    connection = sqlite3.connect("tienda_virtual.db")
    cursor = connection.cursor()

    print("///////// User Registration /////////")

    # We use a loop here so the user stays in the registration
    # screen until they provide valid input. 
    
    while True:
        # .strip() removes accidental spaces at the beginning or end
        full_name = input("Enter your full name: ").strip()
        email = input("Enter your email: ").strip()
        password = input("Enter your password: ").strip()
        role = input("Enter your role (customer/admin): ").strip().lower()

        # --- VALIDATION LINE ---
        if not full_name or not email or not password:
            print("\n[!] Registration Failed: Name, Email, and Password cannot be empty.")
            continue
        # -----------------------

        # Security logic: verify if the role is valid
        if role not in["customer", "admin"]:
            print(f"[SYSTEM] '{role}' is not a valid role. Defaulting to 'customer'.")
            role = "customer"

        try:
            cursor.execute('''
                INSERT INTO User (name, email, password, role) 
                VALUES (?, ?, ?, ?)
            ''', (full_name, email, password, role))

            connection.commit()
            print(f"\nSuccessfully registered user: {full_name}")
            break

        except sqlite3.IntegrityError:
            print("\n[!] Error: This email is already registered.")
        except Exception as e:
            print("\n[!] Error:", e)
            break

    connection.close()

if __name__ == "__main__":
    register_user()