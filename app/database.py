from pymongo import MongoClient, errors

def setup_users_collection():
    client = MongoClient("mongodb+srv://test_user:Dialog!123@cluster0.1fpkz.mongodb.net/?retryWrites=true&w=majority")
    db = client["TESTING"]
    
    # Define the schema
    user_schema = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["first_name", "last_name", "username", "email", "password"],
            "properties": {
                "first_name": {"bsonType": "string", "description": "First name must be a string"},
                "last_name": {"bsonType": "string", "description": "Last name must be a string"},
                "username": {"bsonType": "string", "description": "Username must be a string"},
                "email": {"bsonType": "string", "pattern": "^.+@.+$", "description": "Email must be a valid email address"},
                "password": {"bsonType": "string", "description": "Password must be a hashed string"},
            }
        }
    }

    try:
        # Try creating the collection with schema validation
        db.create_collection("users", validator={"$jsonSchema": user_schema})
    except errors.CollectionInvalid:
        # Collection already exists; modify the validator if supported
        try:
            db.command("collMod", "users", validator={"$jsonSchema": user_schema})
        except errors.OperationFailure as e:
            print("Schema validation not supported or another error:", e)
            print("Proceeding without validation.")
    
    return db["users"]

# Initialize the users collection
users_collection = setup_users_collection()
