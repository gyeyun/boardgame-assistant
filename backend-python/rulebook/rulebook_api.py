# rulebook_api.py

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime

from db.db_connector import SessionLocal
from models.plan import Plan
from models.rulebook import Rulebook
from .rulebook_generator import generate_rulebook_from_prompt
from utils.generate_pdf import render_rulebook_to_pdf

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

# 응답 모델
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

# 룰북 생성 API
@router.post("/api/content/generate-rulebook-script", response_model=RulebookResponse)
def generate_rulebook_from_existing_plan(plan_id: int, db: Session = Depends(get_db)):
    plan = db.query(Plan).filter(Plan.plan_id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="해당 기획안이 없습니다.")

    title, intro, components, age, setup, rule_set, progress, win_condition, turn_order = generate_rulebook_from_prompt(plan.text)

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

# 룰북 PDF 저장 및 다운로드 API
@router.get("/api/content/export-rulebook-pdf")
def export_rulebook_pdf(rulebook_id: int, db: Session = Depends(get_db)):
    rulebook = db.query(Rulebook).filter(Rulebook.rulebook_id == rulebook_id).first()
    if not rulebook:
        raise HTTPException(status_code=404, detail="해당 룰북이 없습니다.")

    context = {
        "title": rulebook.title,
        "intro": rulebook.intro,
        "components": rulebook.components,
        "age": rulebook.age,
        "setup": rulebook.setup,
        "rule_set": rulebook.rule_set,
        "progress": rulebook.progress,
        "win_condition": rulebook.win_condition,
        "turn_order": rulebook.turn_order,
    }

    filename = f"rulebook_{rulebook_id}.pdf"
    pdf_path = render_rulebook_to_pdf(context, filename)

    return FileResponse(pdf_path, media_type="application/pdf", filename=filename)
