from fastapi import APIRouter


# email_auth router
router = APIRouter(tags=["Authentication 🔐"])


@router.post("/signInWithGoogle")
def hello_world():
    return {"message": "hello world"}
