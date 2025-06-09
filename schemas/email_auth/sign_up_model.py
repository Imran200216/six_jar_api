from pydantic import BaseModel, EmailStr

class SignUpModel (BaseModel):
    userName: str 
    userEmail: EmailStr
    userPassword: str