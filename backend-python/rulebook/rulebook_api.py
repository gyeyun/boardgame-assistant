# rulebook_api.py

from models.plan import Plan
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db.db_connector import SessionLocal
from models.rulebook import Rulebook
from datetime import datetime
from .rulebook_generator import generate_rulebook_from_prompt

router = APIRouter()

# DB 세션 DI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 요청 모델 (POST 입력 시 필요 없음)
class RulebookRequest(BaseModel):
    plan_id: int
    prompt: str

# 응답 모델: 모든 항목 포함
class RulebookResponse(BaseModel):
    rulebook_id: int
    title: str
    intro: str
    components: str
    age: str
    setup: str
    rule_set: str
    progress: str
    win_condition: str
    turn_order: str

@router.post("/api/content/generate-rulebook-script", response_model=RulebookResponse)
def generate_rulebook_from_existing_plan(plan_id: int, db: Session = Depends(get_db)):
    # 1. 기획안 가져오기
    plan = db.query(Plan).filter(Plan.plan_id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="해당 기획안이 없습니다.")

    # 2. 룰북 생성
    title, intro, components, age, setup, rule_set, progress, win_condition, turn_order = generate_rulebook_from_prompt(plan.text)

    # 3. DB 저장 (현재는 일부 항목만 저장, 필요시 전체 저장 가능)
    rulebook = Rulebook(
        plan_id=plan.plan_id,
        rule_set=rule_set,
        win_condition=win_condition,
        turn_order=turn_order,
        created_at=datetime.now()
    )
    rulebook = Rulebook(
      plan_id=plan.plan_id,
       title=title,
       intro=intro,
       components=components,
       age=age,
       setup=setup,
       rule_set=rule_set,
       progress=progress,
       win_condition=win_condition,
       turn_order=turn_order,
       created_at=datetime.now()
    )
    db.add(rulebook)
    db.commit()
    db.refresh(rulebook)

    # 4. 응답 반환 (전체 9개 항목)
    return {
        "rulebook_id": rulebook.rulebook_id,
        "title": title,
        "intro": intro,
        "components": components,
        "age": age,
        "setup": setup,
        "rule_set": rule_set,
        "progress": progress,
        "win_condition": win_condition,
        "turn_order": turn_order
    }
