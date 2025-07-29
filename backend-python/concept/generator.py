from datetime import datetime, timezone, timedelta
import random
import json
from utils.openai_utils import call_openai

def generate_concept(theme: str, player_count: str, average_weight: float) -> dict:
    prompt = f"""
다음 정보를 기반으로 보드게임 컨셉을 JSON 형식으로 생성해주세요.

- 장르 또는 분위기: {theme}
- 플레이어 수: {player_count}
- 게임 난이도: {average_weight}

응답은 반드시 아래 형식을 따라야 합니다.
JSON 외 문장은 절대 포함하지 말고, 모든 필드는 정확히 채워주세요.

예시:
{{
    "theme": "전략",
  "playerCount": "2~4명",
  "averageWeight": 3,
  "ideaText": "플레이어는 전략적인 지형을 활용해 상대를 견제하는 턴제 전투를 벌입니다.",
  "mechanics": "지역 점령, 카드 드래프트, 핸드 매니지먼트",
  "storyline": "고대 제국의 후예들이 전설의 유물을 차지하기 위해 맞붙는다."
}}
"""
    response = call_openai(prompt)
    # 터미널로그확인용
    print("LLM 응답:", response)

    try:
        json_start = response.find('{')
        json_end = response.rfind('}') + 1
        json_text = response[json_start:json_end]
        parsed = json.loads(json_text)

        # 시스템에서 직접 생성하는 값
        parsed["conceptId"] = random.randint(1000, 9999)
        parsed["planId"] = random.randint(1000, 9999)

        # KST 기준 createdAt
        kst = timezone(timedelta(hours=9))
        parsed["createdAt"] = datetime.now(kst).isoformat(timespec="seconds")

        return parsed

    except Exception as e:
        print("JSON 파싱 실패:", e)
        return {
            "error": "LLM 응답 파싱 실패",
            "hint": str(e),
            "raw": response
        }

# 재생성
def regenerate_concept(concept_id: int, feedback: str, planId: int) -> dict:
    prompt = f"""
기존 컨셉(conceptId: {concept_id})에 대해 다음 피드백을 반영해 새로운 아이디어를 제시해주세요.

- 피드백: "{feedback}"

응답은 반드시 JSON 형식으로만 반환하세요.  
모든 필드는 아래 예시처럼 완성된 내용으로 채워주세요.

예시:
{{
  "theme": "전략",
  "playerCount": "2~4명",
  "averageWeight": 2.5,
  "ideaText": "플레이어는 전략적인 지형을 활용해 상대를 견제하는 턴제 전투를 벌입니다.",
  "mechanics": "지역 점령, 카드 드래프트, 핸드 매니지먼트",
  "storyline": "고대 제국의 후예들이 전설의 유물을 차지하기 위해 맞붙는다."
}}
"""
    response = call_openai(prompt)

    try:
        # JSON 파싱 후 필드 보강
        json_start = response.find('{')
        json_end = response.rfind('}') + 1
        json_text = response[json_start:json_end]
        parsed = json.loads(json_text)

        parsed["conceptId"] = random.randint(1000, 9999)  # 새 컨셉 ID
        parsed["planId"] = planId #기존 아이디
        parsed["createdAt"] = datetime.now(timezone(timedelta(hours=9))).isoformat(timespec="seconds")

        return parsed

    except Exception as e:
        return {
            "error": "LLM 응답 파싱 실패",
            "hint": str(e),
            "raw": response
        }
    
# 컨셉 기반 요소 생성
# 임시데이터로 수정 필요
plan_store = {
    1012: {
    "conceptId": 1001,
    "theme": "전략",
    "playerCount": "2~4명",
    "averageWeight": 3,
    "ideaText": "플레이어는 전략적인 지형을 활용해 상대를 견제하는 턴제 전투를 벌입니다.",
    "mechanics": "지역 점령, 카드 드래프트, 핸드 매니지먼트",
    "storyline": "고대 제국의 후예들이 전설의 유물을 차지하기 위해 맞붙는다.",
    "createdAt": "2025-07-24T15:00:00"
    }
}

def generate_components(plan_id: int) -> dict:
    # 플랜 조회
    plan_data = plan_store.get(plan_id)
    if plan_data is None:
        return {
            "error": "존재하지 않는 planId입니다.",
            "hint": f"conceptId {plan_id} 에 해당하는 컨셉이 없습니다."
        }

    prompt = f"""
기획 정보를 기반으로 보드게임의 상세 설계 요소를 생성해주세요.

기획 정보:
- 테마: {plan_data['theme']}
- 인원 수: {plan_data['playerCount']}
- 난이도: {plan_data['averageWeight']}
- ideaText: {plan_data['ideaText']}
- 스토리라인: {plan_data['storyline']}
- 매커니즘 : {plan_data['mechanics']}

반드시 아래 구조의 JSON 하나로만 반환해주세요:

예시:
예시 형식:
{{
  "components": [
    {{
      "type": "토큰",
      "name": "시간 조각 토큰",
      "effect": "점수 계산에 사용",
      "visualType": "3D"
    }},
    {{
      "type": "카드",
      "name": "마법 봉인 카드",
      "effect": "상대방의 다음 행동을 무효화합니다.",
      "visualType": "2D"
    }},
    {{
      "type": "보드",
      "name": "비밀 통로 보드",
      "effect": "특정 위치를 통해 빠르게 이동할 수 있습니다.",
      "visualType": "2D"
    }}
  ]
}}
"""
    response = call_openai(prompt)

    try:
        # JSON 파싱 후 필드 보강
        json_start = response.find('{')
        json_end = response.rfind('}') + 1
        json_text = response[json_start:json_end]
        parsed = json.loads(json_text)

        return parsed

    except Exception as e:
        return {
            "error": "LLM 응답 파싱 실패",
            "hint": str(e),
            "raw": response
        }