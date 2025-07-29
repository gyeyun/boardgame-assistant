from pydantic import BaseModel
from typing import List
from datetime import datetime

# dto
class ConceptGenerateRequest(BaseModel):
    theme: str
    playerCount: str
    averageWeight: float

class ConceptGenerateResponse(BaseModel):
    conceptId: int
    planId: int
    theme: str
    playerCount: str
    averageWeight: float
    ideaText: str
    mechanics: str
    storyline: str
    createdAt: datetime

# 재생성
class ConceptRegenerateRequest(BaseModel):
    conceptId: int
    planId: int
    feedback: str

# 컨셉기반요소생성
class ComponentRequest(BaseModel):
    planId: int


class Component(BaseModel): 
    type: str # 예: "토큰", "카드", "보드" 
    name: str # 예: "에너지 토큰" 
    effect: str # 기능 또는 설명 
    visualType: str # 예: "2D", "3D" 

class ComponentResponse(BaseModel):
    components: List[Component]
