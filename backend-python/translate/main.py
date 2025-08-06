import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

app = FastAPI()

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
    99: "안녕하세요, 보드게임을 시작해볼까요?"
}

next_content_id = max(dummy_contents.keys()) + 1

@app.post("/api/translate/request", response_model=TranslationResponse)
async def translate_content(request: TranslationRequest):
    global next_content_id

    original_text = dummy_contents.get(request.contentId)
    if not original_text:
        raise HTTPException(status_code=404, detail="Content not found")

    prompt = f"Translate the following text to {request.targetLanguage}:\n\n{original_text}"

    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        translated_text = completion.choices[0].message.content.strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")

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
#cd backend-python/translate
#uvicorn main:app --reload
#http POST http://localhost:8000/api/translate/request contentId=99 targetLanguage=en
#http GET http://localhost:8000/api/translate/content/100