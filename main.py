from fastapi import FastAPI

# Firebase
from config.firebase_config import init_firebase

# MongoDB
from config.mongo_db_config import init_mongodb


# Logger
from config.logging_config import logger

# env
from dotenv import load_dotenv


# Load Env
load_dotenv()


# ✅ Initialize Firebase & MongoDB
init_firebase()
init_mongodb()


# Import routers
from auth.apple_auth import router as apple_router
from auth.email_auth import router as email_router
from auth.google_auth import router as google_router
from currency.currency_selected import router as currency_selected_router
from income.add_income import router as add_income_router
from income.get_all_income_history import router as get_all_income_history_router
from jar_expense.add_jar_expense import router as add_jar_expense_router
from jar_expense.get_all_jar_expense_history import router as get_all_jar_expense_router

# ✅ Setup FastAPI
app = FastAPI(title="Six Jar App End Point 👽💥")

# ✅ Include routers
app.include_router(apple_router, prefix="/auth")
app.include_router(email_router, prefix="/auth")
app.include_router(google_router, prefix="/auth")
app.include_router(currency_selected_router, prefix="/currency")
app.include_router(add_income_router, prefix="/income")
app.include_router(get_all_income_history_router, prefix="/income")
app.include_router(add_jar_expense_router, prefix="/jarExpense")
app.include_router(get_all_jar_expense_router, prefix="/jarExpense")


logger.info("🚀 FastAPI server started and all routers registered.")
