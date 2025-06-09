from pydantic import BaseModel, EmailStr

class UserModel (BaseModel):
    firebase_uid : str 
    userName: str
    userEmail : EmailStr