from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from evaluator1 import evaluate_balance

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

class GameData(BaseModel):
    difficulty: str
    player_count: str
    main_objectives: List[str]
    rules: List[str]
    win_conditions: List[str]
    fail_conditions: List[str]

class BalanceAnalysis(BaseModel):
    simulationSummary: str
    issuesDetected: List[str]
    recommendations: List[str]
    balanceScore: float

class BalanceFeedbackResponse(BaseModel):
    balanceAnalysis: BalanceAnalysis

@app.get("/")
async def read_index():
    return FileResponse('static/test.html')

@app.post("/api/feedback/balance", response_model=BalanceFeedbackResponse)
async def evaluate(game_data: GameData):
    game_dict = game_data.model_dump()
    result = evaluate_balance(game_dict)
    return result
#cd backend-python/balance
#uvicorn main:app --reload