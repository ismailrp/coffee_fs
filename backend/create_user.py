from app.database import SessionLocal

from app.models.user import User

from app.auth.password_handler import hash_password

db = SessionLocal()

user = User(
    username="admin",
    password=hash_password("admin123")
)

db.add(user)

db.commit()

print("User created")