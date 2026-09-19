from app.database import init_db, query_one, execute
from app.models.enums import UserRole
from app.models.user import User
from datetime import datetime
from getpass import getpass

init_db()

if query_one("SELECT * FROM USERS WHERE role = ?", (UserRole.ADMIN.value,)):
    raise ValueError("Admin user already exists!")

name = input("Enter admin name: ")

while True:
    email = input("Enter admin email: ")
    if User._validate_email(email):
        break
    print("Invalid email. Please try again.")

while True:
    password = getpass("Enter admin password: ")
    is_valid, message = User._validate_password(password)
    if is_valid:
        break
    print(f"Invalid password: {message}. Please try again.")

password_hash = User._hash_password(password)

execute("INSERT INTO USERS (name, email, password_hash, role, is_active, created_at) VALUES (?, ?, ?, ?, ?, ?)", (name, email, password_hash, UserRole.ADMIN.value, True, datetime.now().isoformat()))