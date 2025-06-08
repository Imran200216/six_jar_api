from fastapi import APIRouter

router = APIRouter(tags=["Income 💵"])


# User Add Income (Store the data in MongoDB as User Collection)
@router.post("/add_income")
async def userSelectedCurrency():
    return {
        "message": "user selected",
    }


