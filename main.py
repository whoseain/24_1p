from fastapi import FastAPI, HTTPException
from app.model import UserRegister, UserLogin
from app.database import get_user_collection
from app.auth import hash_password, user_exists, verify_password

app = FastAPI()

users_collection = get_user_collection()

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

@app.post("/login")
def login_user_route(user: UserLogin):
    user_record = users_collection.find_one({"username": user.username})
    if user_record is None or not verify_password(user.password, user_record["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return {
        "username": user.username,
        "status": "success",
        "message": "User logged in successfully"
    }

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}
