# FastAPI API 라우터
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db.db_connector import SessionLocal
from models.rulebook import Rulebook
from models.content import Content
from datetime import datetime
from .description_generator import generate_description_script
from utils.generate_pdf import render_description_to_pdf
from typing import List

router = APIRouter()

# DB 세션 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 요청 모델
class DescriptionRequest(BaseModel):
    rulebook_id: int
    plan_id: int
    project_id: int

# 응답 모델
class DescriptionResponse(BaseModel):
    script: str

# 설명 스크립트 생성 + 저장 API
@router.post("/api/content/generate-description-script", response_model=DescriptionResponse)
def create_description_script(request: DescriptionRequest, db: Session = Depends(get_db)):
    rulebook: Rulebook = db.query(Rulebook).filter(Rulebook.rulebook_id == request.rulebook_id).first()
    if not rulebook:
        raise HTTPException(status_code=404, detail="룰북이 존재하지 않습니다.")
    
    rulebook_text = f"{rulebook.rule_set}\n승리 조건: {rulebook.win_condition}\n턴 순서: {rulebook.turn_order}"
    script = generate_description_script(rulebook_text)

    content = Content(
        plan_id=request.plan_id,
        project_id=request.project_id,
        contentType="description_script",
        data=script,
        created_at=datetime.now(),
        submitted_at=datetime.now()
    )
    db.add(content)
    db.commit()
    db.refresh(content)

    return {"script": script}

# 저장된 스크립트 전체 조회 API
@router.get("/api/content", response_model=List[DescriptionResponse])
def get_all_scripts(db: Session = Depends(get_db)):
    contents = db.query(Content).filter(Content.contentType == "description_script").all()
    return [{"script": c.data} for c in contents]

# 설명 스크립트 PDF 다운로드 API
@router.get("/api/content/export-description-pdf")
def export_description_pdf(content_id: int, db: Session = Depends(get_db)):
    content = db.query(Content).filter(Content.content_id == content_id).first()
    if not content or content.contentType != "description_script":
        raise HTTPException(status_code=404, detail="설명 스크립트가 존재하지 않습니다.")
    
    filename = f"description_{content_id}.pdf"
    pdf_path = render_description_to_pdf(content.data, filename)

    return FileResponse(pdf_path, media_type="application/pdf", filename=filename)
