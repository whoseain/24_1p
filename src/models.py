
from pydantic import BaseModel

class UserRegister(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str
