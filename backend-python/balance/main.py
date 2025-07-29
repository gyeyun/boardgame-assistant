from fastapi import FastAPI
from pydantic import BaseModel
from evaluator1 import evaluate_balance
from typing import List
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
#uvicorn main:app --reload
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

class GameData(BaseModel):
    difficulty: str
    player_count: str
    main_objectives: List[str]
    rules: List[str]
    win_conditions: List[str]
    fail_conditions: List[str]
#테스트용
@app.get("/")
async def read_index():
    return FileResponse('static/test.html')

@app.post("/evaluate")
async def evaluate(game_data: GameData) -> dict:
    game_dict = game_data.model_dump() 
    result = evaluate_balance(game_dict)
    return {"evaluation_result": result}




