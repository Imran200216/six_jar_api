from fastapi import APIRouter

router = APIRouter(tags=["Jar Expense 💰"])


# Add Expense Jar For Particular Jars
@router.post("/add_jar_expense")
async def addExpenseJar():
    return {
        "message": "user selected",
    }
