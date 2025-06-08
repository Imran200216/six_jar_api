from fastapi import APIRouter

router = APIRouter(tags=["Jar Expense 💰"])


# Add Expense Jar For Particular Jars
@router.post("/get_all_jar_exense_history")
async def addExpenseJar():
    return {
        "message": "user selected",
    }
