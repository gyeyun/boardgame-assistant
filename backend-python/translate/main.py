from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sys
import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.openai_utils import call_openai

app = FastAPI()

origins = [
    "http://localhost:8080", # 스프링 부트 서버 주소
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", include_in_schema=False)
async def read_index():
    return FileResponse(os.path.join(os.path.dirname(__file__), 'index.html'))

class TranslationRequest(BaseModel):
    contentId: int
    targetLanguage: str

class TranslationResponse(BaseModel):
    translatedContentId: int
    status: str

class TranslationContent(BaseModel):
    contentId: int
    text: str

dummy_contents = {
    99: """게임 목표:
가장 먼저 15 명성 포인트를 모으는 것이 목표입니다.

게임 구성:
- 보석 토큰 (에메랄드, 사파이어, 루비, 다이아몬드, 오닉스) 각 7개
- 황금 조커 토큰 5개
- 개발 카드: 레벨 1, 2, 3 각 40장
- 귀족 타일: 총 10장 중 플레이어 수에 따라 사용

게임 방식:
1. 자신의 차례에는 다음 중 하나의 행동을 합니다:
   - 서로 다른 보석 3개 가져오기
   - 같은 보석 2개 가져오기 (해당 보석이 4개 이상 남아있을 때)
   - 개발 카드 예약 및 황금 토큰 1개 받기
   - 개발 카드 구매

2. 개발 카드는 보석 할인과 명성 포인트를 제공합니다.
3. 귀족 타일은 일정한 조건을 만족하면 자동으로 획득되어 추가 점수를 줍니다.

게임 종료:
한 플레이어가 15점 이상을 획득하면, 해당 라운드까지 모두 진행 후 가장 점수가 높은 플레이어가 승리합니다.
"""
}


next_content_id = max(dummy_contents.keys()) + 1

@app.post("/api/translate/request", response_model=TranslationResponse)
async def translate_content(request: TranslationRequest):
    global next_content_id

    original_text = dummy_contents.get(request.contentId)
    if not original_text:
        raise HTTPException(status_code=404, detail="Content not found")

    prompt = f"Translate the following text to {request.targetLanguage}:\n\n{original_text}"

    translated_text = call_openai(prompt)

    if not translated_text:
        raise HTTPException(status_code=500, detail="Translation failed")

    translated_content_id = next_content_id
    dummy_contents[translated_content_id] = translated_text
    next_content_id += 1

    return TranslationResponse(
        translatedContentId=translated_content_id,
        status="pending_review"
    )

@app.get("/api/translate/content/{content_id}", response_model=TranslationContent)
async def get_translated_content(content_id: int):
    text = dummy_contents.get(content_id)
    if not text:
        raise HTTPException(status_code=404, detail="Content not found")
    return TranslationContent(contentId=content_id, text=text)

