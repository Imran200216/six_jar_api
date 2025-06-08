from fastapi import APIRouter


# email_auth router 
router = APIRouter(tags=["Authentication 🔐"])

# SignUp With Email Password
@router.post("/signUpWithEmailPassword")
def hello_world():
    return {"message": "hello world"}


# SignIn With Email Password 
@router.post("/signInWithEmailPassword")
def hello_world():
    return {"message": "hello world"}

# Forget Password 
@router.post("/forgetPassword")
def hello_world():
    return {"message": "hello world"}