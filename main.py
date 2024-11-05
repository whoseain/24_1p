
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from passlib.context import CryptContext

app = FastAPI()

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# MongoDB connection
client = MongoClient("mongodb+srv://test_user:Dialog!123@cluster0.1fpkz.mongodb.net/?retryWrites=true&w=majority")
db = client["TESTING"]
users_collection = db["users"]

# Hash the password
def hash_password(password: str):
    return pwd_context.hash(password)

# Check if user already exists in the database
def user_exists(email: str, username: str):
    return users_collection.find_one({"$or": [{"email": email}, {"username": username}]}) is not None

# Updated User registration data model
class UserRegister(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str
    password: str

# User login data model
class UserLogin(BaseModel):
    username: str
    password: str

# Register a single user
@app.post("/register")
def register_user(user: UserRegister):
    if user_exists(user.email, user.username):
        raise HTTPException(status_code=400, detail="User with this email or username already exists")

    hashed_password = hash_password(user.password)
    new_user = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "email": user.email,
        "password": hashed_password
    }
    
    users_collection.insert_one(new_user)
    return {"message": "User registered successfully"}

# User login route using username instead of email
@app.post("/login")
def login_user_route(user: UserLogin):
    user_record = users_collection.find_one({"username": user.username})
    if user_record is None or not pwd_context.verify(user.password, user_record["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return {
        "username": user.username,
        "status": "success",
        "message": "User logged in successfully"
    }

# Root route
@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}
