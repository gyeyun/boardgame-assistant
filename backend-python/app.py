from fastapi import FastAPI
from description import description_api
from rulebook import rulebook_api
from utils.send_to_spring import send_to_spring



app = FastAPI()

# 설명 스크립트 API 라우터 등록
app.include_router(description_api.router)

app.include_router(rulebook_api.router)
