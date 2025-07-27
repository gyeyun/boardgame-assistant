from fastapi import APIRouter
from rule.schema import RuleGenerateRequest, RuleGenerateResponse, RuleRegenerateRequest
from rule.generator import generate_rule, regenerate_rule

router = APIRouter(prefix="/api/plans")

@router.post("/generate-rule", response_model=RuleGenerateResponse)
def generate_rule_api(req: RuleGenerateRequest):
    return generate_rule(req.conceptId)

@router.post("/regenerate-rule", response_model=RuleGenerateResponse)
def regenerate_rule_api(req: RuleRegenerateRequest):
    return regenerate_rule(req.ruleId, req.feedback)