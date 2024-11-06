from passlib.context import CryptContext
from app.database import get_user_collection

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
users_collection = get_user_collection()

# Hash the password
def hash_password(password: str):
    return pwd_context.hash(password)

# Verify the password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Check if user already exists in the database
def user_exists(email: str, username: str):
    return users_collection.find_one({"$or": [{"email": email}, {"username": username}]}) is not None
