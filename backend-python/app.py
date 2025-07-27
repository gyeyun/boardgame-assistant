from fastapi import FastAPI
from rule.router import router as rule_router

app = FastAPI()
app.include_router(rule_router)