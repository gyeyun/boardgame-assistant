import json
from utils.openai_utils import call_openai
import random


#임시 데이터로(concept_store) 수정필요
concept_store = {
    5566: {
        "theme": "요리경쟁",
        "playerCount": "2명",
        "averageWeight": 2.3,
        "ideaText": "플레이어는 주어진 재료를 활용하여 레시피를 완성하고 심사위원들의 평가를 받는 요리 대회를 펼칩니다.",
        "mechanics": "재료 수집, 레시피 완성, 심사 평가",
        "storyline": "세계적인 요리 대회에 참가한 플레이어들이 최고의 요리를 만들어서 우승을 차지하기 위해 경쟁합니다."
    }
}


def generate_rule(concept_id: int) -> dict:
    # 컨셉 조회
    concept_data = concept_store.get(concept_id)
    if concept_data is None:
        return {
            "error": "존재하지 않는 conceptId입니다.",
            "hint": f"conceptId {concept_id} 에 해당하는 컨셉이 없습니다."
        }
    
    prompt = f"""
컨셉 정보를 기반으로 보드게임의 게임규칙을 생성해주세요.

컨셉 정보:
- 테마: {concept_data['theme']}
- 아이디어: {concept_data['ideaText']}
- 메커닉: {concept_data['mechanics']}
- 스토리라인: {concept_data['storyline']}


응답은 반드시 아래 형식을 따라야 합니다.
JSON 외에는 아무 문장도 포함하지 마세요.

예시:
{{
  "turnStructure": "1. 자원 수집 → 2. 행동 선택 → 3. 전투 또는 협상 → 4. 턴 종료 처리",
  "actionRules": [
    "자원 수집 시 무작위 카드 2장과 1 토큰 획득",
    "상대 진영과 협상 시 거래 조건을 비공개로 제안 가능",
    "전투 시 주사위로 결과 결정, 추가 카드 사용 가능"
  ],
  "victoryCondition": "유물을 3개 먼저 수집하면 즉시 승리",
  "penaltyRules": [
    "자원이 0일 때 행동 제한 발생",
    "동맹을 배신할 경우 다음 2턴간 협상 불가"
  ],
  "designNote": "게임 흐름이 직관적이면서도, 협상과 배신이 자연스럽게 녹아들도록 구조화함"
}}
"""
    response = call_openai(prompt)
    # print("LLM 응답:", response)

    try:
        # 응답에서 JSON만 추출 (앞뒤에 문장이 붙을 수 있음)
        json_start = response.find('{')
        json_end = response.rfind('}') + 1
        json_text = response[json_start:json_end]
        parsed = json.loads(json_text)

        #룰 ID 생성 및 삽입(랜덤으로 우선처리)
        parsed["ruleId"] = random.randint(3000, 9999)

        #키가 빈 경우
        parsed.setdefault("turnStructure", "")
        parsed.setdefault("actionRules", [])
        parsed.setdefault("victoryCondition", "")
        parsed.setdefault("penaltyRules", [])
        parsed.setdefault("designNote", "")

        return parsed
    
    except Exception as e:
        print("JSON 파싱 실패:", e)
        return {
            "error": "LLM 응답 파싱 실패",
            "hint": str(e),
            "raw": response
        }