from pydantic import BaseModel, EmailStr

class ForgetPasswordModel (BaseModel):
    userEmail: EmailStr