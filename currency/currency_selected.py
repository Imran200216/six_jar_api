from fastapi import APIRouter

router = APIRouter(tags=["Currency 💱"])


# User Currency Selected
@router.put("/currency_selected")
async def userSelectedCurrency():
    return {
        "message": "user selected",
    }
