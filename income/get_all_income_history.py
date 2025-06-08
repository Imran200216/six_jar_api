from fastapi import APIRouter

router = APIRouter(tags=["Income 💵"])


# User Get Income History
@router.get("/user_income_history")
async def userIncomeHistory():
    return {
        "message": "Fetch User Income History",
    }
