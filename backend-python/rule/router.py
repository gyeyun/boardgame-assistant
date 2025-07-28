from fastapi import APIRouter
from rule.schema import RuleGenerateRequest, RuleGenerateResponse, RuleRegenerateRequest, RuleSimulationResponse, RuleSimulationRequest

# 규칙 생성, 재쟁성
from rule.generator import generate_rule, regenerate_rule
# 규칙 시뮬레이션
from rule.simulator import rule_test


router = APIRouter(prefix="/api")

@router.post("/plans/generate-rule", response_model=RuleGenerateResponse)
def generate_rule_api(req: RuleGenerateRequest):
    return generate_rule(req.conceptId)

@router.post("/plans/regenerate-rule", response_model=RuleGenerateResponse)
def regenerate_rule_api(req: RuleRegenerateRequest):
    return regenerate_rule(req.ruleId, req.feedback)

@router.post("simulate/rule-test", response_model=RuleSimulationResponse)
def rule_test_api(req: RuleSimulationRequest):
    return rule_test( req.ruleId,
        req.playerNames,
        req.maxTurns,
        req.enablePenalty)