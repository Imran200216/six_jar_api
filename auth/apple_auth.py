from fastapi import APIRouter


# apple_auth router
router = APIRouter(tags=["Authentication 🔐"])


@router.post("/signInWithApple")
def hello_world():
    return {"message": "hello world"}
