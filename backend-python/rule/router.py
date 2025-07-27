from fastapi import APIRouter
from rule.schema import RuleGenerateRequest, RuleGenerateResponse
from rule.generator import generate_rule

router = APIRouter(prefix="/api/plans")

@router.post("/generate-rule", response_model=RuleGenerateResponse)
def generate_goal_api(req: RuleGenerateRequest):
    return generate_rule(req.conceptId)