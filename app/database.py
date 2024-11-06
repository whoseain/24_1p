from pymongo import MongoClient

def get_user_collection():
    client = MongoClient("mongodb+srv://test_user:Dialog!123@cluster0.1fpkz.mongodb.net/?retryWrites=true&w=majority")
    db = client["TESTING"]
    return db["users"]
