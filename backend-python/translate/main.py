from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sys
import os
from fastapi.middleware.cors import CORSMiddleware

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

# --- API 모델 (스프링과 연동하기 위한 모델) ---
class TranslationRequest(BaseModel):
    text_to_translate: str
    target_language: str

class TranslationResponse(BaseModel):
    translated_text: str

# --- API 엔드포인트 (단순화) ---
@app.post("/api/translate/request", response_model=TranslationResponse)
async def translate_content(request: TranslationRequest):
    """
    스프링으로부터 텍스트를 직접 받아 번역하고, 결과를 즉시 반환합니다.
    """
    prompt = f"Translate the following Korean text to {request.target_language}:\n\n{request.text_to_translate}"
    
    translated_text = call_openai(prompt)

    if not translated_text:
        raise HTTPException(status_code=500, detail="Translation from AI service failed")

    return TranslationResponse(translated_text=translated_text)
