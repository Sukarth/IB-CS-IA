from app.database import init_db, query_one, execute
from app.models.enums import UserRole
from app.models.user import User
from datetime import datetime
from getpass import getpass
import sys

def create_admin():
    init_db()
    
    if query_one("SELECT * FROM USERS WHERE role = ?", (UserRole.ADMIN.value,)):
        print("Admin user already exists!")
        sys.exit(1)
    
    name = input("Enter admin name: ")
    
    while True:
        email = input("Enter admin email: ").strip().lower()
        if User._validate_email(email):
            if not query_one("SELECT * FROM USERS WHERE email = ?", (email,)):
                break
            else:
                print("Email is already in use. Please try again.")
            
        print("Invalid email. Please try again.")
        
        
    
    while True:
        password = getpass("Enter admin password: ")
        is_valid, message = User._validate_password(password)
        if is_valid:
            break
        print(f"Invalid password: {message}. Please try again.")
    
    while True:
        confirm_password = getpass("Retype admin password to confirm: ")
        if password == confirm_password:
            break
        print("Passwords do not match. Please try again.")
    
    password_hash = User._hash_password(password)
    
    execute("INSERT INTO USERS (name, email, password_hash, role, is_active, created_at) VALUES (?, ?, ?, ?, ?, ?)", (name, email, password_hash, UserRole.ADMIN.value, True, datetime.now().isoformat()))

    print("Admin user created successfully.")

if __name__ == "__main__":
    create_admin()    
    