import json
from utils.openai_utils import call_openai
from typing import List
import random


# 룰 임시 데이터
rule_store = {
    101: {
    "turnStructure": "각 턴마다 모든 플레이어가 순차적으로 행동을 수행한다.",
    "actionRules": [
      "자원 수집은 점수를 획득하거나 다음 행동에 필요한 조건을 충족시킨다.",
      "탐색은 새로운 기회를 발견하거나 위험 요소를 노출시킨다.",
      "교섭은 상대방과의 관계를 조정하며 점수에 영향을 줄 수 있다.",
      "전투 개시는 상대방과의 직접적인 경쟁을 유발하며 승패에 큰 영향을 준다."
  ],
    "penaltyRules": [
      "행동 실패 시 점수 차감 또는 턴 소모",
      "전투 패배 시 추가 페널티 발생"
    ],
    "victoryCondition": "총 점수가 높은 플레이어가 승리하며, 동점일 경우 더 적은 턴을 사용한 플레이어가 승리한다.",
    "designNote": "이 룰셋은 전략적 자원 관리와 상호작용 중심의 턴 기반 게임을 시뮬레이션하기 위해 설계됨."
  }
}

# 시뮬레이션, 규칙 테스트
def rule_test(rule_id: int, player_names: List[str], max_turns: int, enable_penalty: bool) -> dict:
    # 룰 조회
    rule_data = rule_store.get(rule_id)
    if rule_data is None:
        return {
            "error": "존재하지 않는 rule_Id입니다.",
            "hint": f"ruleId {rule_id} 에 해당하는 컨셉이 없습니다."
        }

    prompt = f"""
      규칙 정보를 기반으로 보드게임의 시뮬레이션 결과 생성해주세요.

      규칙 정보:
      - 턴 구조: {rule_data['turnStructure']}
      - 주요 행동 규칙: {"; ".join(rule_data['actionRules'])}
      - 페널티 규칙: {"; ".join(rule_data['penaltyRules']) if enable_penalty else "페널티 규칙은 사용하지 않습니다."}
      - 승리 조건: {rule_data['victoryCondition']}

      시뮬레이션 조건:
      - 플레이어: {", ".join(player_names)}
      - 최대 턴 수: {max_turns}
      - 페널티 적용 여부: {"적용" if enable_penalty else "미적용"}

      응답은 반드시 아래 형식을 따라야 합니다.
      JSON 외에는 아무 문장도 포함하지 마세요.

      예시:
      {{
          "simulationHistory": [
            {{
              "gameId": 1,
              "turns": [
                {{ "turn": 1, "actions": ["Player A: 자원 수집", "Player B: 탐색"] }},
                {{ "turn": 2, "actions": ["Player A: 교섭", "Player B: 전투 개시"] }}
                ...
              ],
              "winner": "Player B",
              "totalTurns": 9,
              "durationMinutes": 35,
              "score": {{ "Player A": 8, "Player B": 12 }}
            }},
            {{
              "gameId": 2,
              ...
            }}
          ]
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
        parsed["gameId"] = random.randint(3000, 9999)

        #키가 빈 경우
        parsed.setdefault("simulationHistory", [])
        parsed.setdefault("turnStructure", "")
        parsed.setdefault("actionRules", [])
        parsed.setdefault("penaltyRules", [])
        parsed.setdefault("victoryCondition", "")
        parsed.setdefault("designNote", "")

        return parsed
    
    except Exception as e:
        print("JSON 파싱 실패:", e)
        return {
            "error": "LLM 응답 파싱 실패",
            "hint": str(e),
            "raw": response
        }
