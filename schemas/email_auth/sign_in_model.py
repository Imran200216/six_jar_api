from pydantic import BaseModel, EmailStr

class SignInModel (BaseModel):
    userEmail: EmailStr
    userPassword: str