#API 라우터
from models.plan import Plan
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db.db_connector import SessionLocal
from models.rulebook import Rulebook
from datetime import datetime
from .rulebook_generator import generate_rulebook_from_prompt

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class RulebookRequest(BaseModel):
    plan_id: int
    prompt: str

class RulebookResponse(BaseModel):
    rulebook_id: int
    rule_set: str
    win_condition: str
    turn_order: str

@router.post("/api/content/generate-rulebook-script", response_model=RulebookResponse)
def generate_rulebook_from_existing_plan(plan_id: int, db: Session = Depends(get_db)):
    # 1. 기획안 조회
    plan = db.query(Plan).filter(Plan.plan_id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="해당 기획안이 없습니다.")

    # 2. 기획안 내용을 기반으로 룰북 생성
    rule_set, win_condition, turn_order = generate_rulebook_from_prompt(plan.text)

    # 3. 생성된 룰북 저장
    rulebook = Rulebook(
        plan_id=plan.plan_id,
        rule_set=rule_set,
        win_condition=win_condition,
        turn_order=turn_order,
        created_at=datetime.now()
    )
    db.add(rulebook)
    db.commit()
    db.refresh(rulebook)

    return {
        "rulebook_id": rulebook.rulebook_id,
        "rule_set": rule_set,
        "win_condition": win_condition,
        "turn_order": turn_order
    }
