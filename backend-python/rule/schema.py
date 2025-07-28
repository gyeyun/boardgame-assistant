from pydantic import BaseModel
from typing import List, Dict
from dataclasses import dataclass

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


# dto - 게임 규칙 재생성
class RuleRegenerateRequest(BaseModel):
   ruleId: int
   feedback: str

# dto - 규칙 시뮬레이션 
@dataclass
class Turn:
    turn: int
    actions: List[str]

class RuleSimulationRequest(BaseModel):
        ruleId: int
        playerNames: List[str]
        maxTurns: int
        enablePenalty: bool #패널티규칙 적용여부

class SimulationResult(BaseModel):
    gameId: int
    turns: List[Turn]
    winner: str
    totalTurns: int
    durationMinutes: int
    score: Dict[str, int] #어떤 플레이어가 어떤 점수를 얻었는지 구분하기 위해 딕셔너리 사용.

class RuleSimulationResponse(BaseModel): 
    simulationHistory: List[SimulationResult]