from pydantic import BaseModel
from typing import List

# dto - 게임 규칙 자동생성
class RuleGenerateRequest(BaseModel):
   conceptId: int

class RuleGenerateResponse(BaseModel):
    ruleId: int
    turnStructure: str
    actionRules: List[str]
    penaltyRules: List[str]
    victoryCondition: str
    designNote: str