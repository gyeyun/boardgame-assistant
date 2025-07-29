from fastapi import APIRouter
from concept.schema import ConceptGenerateRequest, ConceptGenerateResponse, ConceptRegenerateRequest, ComponentRequest, ComponentResponse
from concept.generator import generate_concept, regenerate_concept, generate_components

router = APIRouter(prefix="/api/plans")

@router.post("/generate-concept", response_model=ConceptGenerateResponse)
def generate_concept_api(req: ConceptGenerateRequest):
    return generate_concept(req.theme, req.playerCount, req.averageWeight)

@router.post("/regenerate-concept", response_model=ConceptGenerateResponse)
def regenerate_concept_api(req: ConceptRegenerateRequest):
    return regenerate_concept(req.conceptId, req.feedback, req.planId)

@router.post("/generate-components", response_model=ComponentResponse)
def generate_components_api(req: ComponentRequest):
    return generate_components(req.planId)

