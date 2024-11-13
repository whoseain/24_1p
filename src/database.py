from pymongo import MongoClient
from passlib.context import CryptContext

# MongoDB connection
client = MongoClient("mongodb+srv://test_user:Dialog!123@cluster0.1fpkz.mongodb.net/?retryWrites=true&w=majority")
db = client["TESTING"]
users_collection = db["users"]

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash the password
def hash_password(password: str):
    return pwd_context.hash(password)

# Check if user already exists in the database
def user_exists(email: str, username: str):
    return users_collection.find_one({"$or": [{"email": email}, {"username": username}]}) is not None

# Insert a new user
def insert_user(user_data: dict):
    users_collection.insert_one(user_data)

# Find user by username
def find_user(username: str):
    return users_collection.find_one({"username": username})
