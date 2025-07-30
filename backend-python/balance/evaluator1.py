import os
from openai import OpenAI
from dotenv import load_dotenv
from collections import OrderedDict

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def evaluate_balance(game_data: dict) -> dict:
    prompt = f"""
    당신은 전문 보드게임 디자이너이자 시뮬레이션 설계자입니다.

    다음은 보드게임의 구성 요소입니다:

    - 난이도: {game_data["difficulty"]}
    - 인원: {game_data["player_count"]}
    - 주요 목표: {', '.join(game_data["main_objectives"])}
    - 행동 규칙: {', '.join(game_data["rules"])}
    - 승리 조건: {', '.join(game_data["win_conditions"])}
    - 패배/탈락 조건: {', '.join(game_data["fail_conditions"])}

    이제 당신은 **이 게임을 머릿속으로 직접 시뮬레이션**해 보며 다음을 평가해야 합니다:

    1. 시뮬레이션 요약 (게임 평균 시간, 승리 점수 등 통계적 요약)
    2. 문제점 감지 (밸런스 붕괴, 특정 전략 독점 등)
    3. 개선 제안 (룰 수정, 역할 능력 조정 등)
    4. 밸런스 점수 (10점 만점)

    아래 JSON 형식으로 응답하세요. **키 순서를 반드시 다음으로 유지**: simulationSummary, issuesDetected, recommendations, balanceScore.

    {{
      "balanceAnalysis": {{
        "simulationSummary": "문장으로 요약",
        "issuesDetected": ["문제1", "문제2"],
        "recommendations": ["제안1", "제안2"],
        "balanceScore": 숫자
      }}
    }}

    **응답 예시**:
    {{
      "balanceAnalysis": {{
        "simulationSummary": "총 20회 플레이 테스트 결과, 평균 게임 시간은 38분이며, 평균 승리 점수는 12점이었습니다.",
        "issuesDetected": ["일부 플레이어가 첫 턴부터 유리한 자원을 독점함", "‘탐색가’ 역할의 승률이 60%로 지나치게 높음"],
        "recommendations": ["초기 자원 분배를 균등 분배 방식으로 수정 필요", "‘탐색가’ 능력 조정 제안 (탐색 범위 축소 등)"],
        "balanceScore": 6.7
      }}
    }}
    """

    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )

    import json
    response_text = chat_completion.choices[0].message.content
    try:
        # JSON 파싱
        response_dict = json.loads(response_text)
        # 키 순서 보장
        ordered_balance_analysis = OrderedDict([
            ("simulationSummary", response_dict["balanceAnalysis"]["simulationSummary"]),
            ("issuesDetected", response_dict["balanceAnalysis"]["issuesDetected"]),
            ("recommendations", response_dict["balanceAnalysis"]["recommendations"]),
            ("balanceScore", response_dict["balanceAnalysis"]["balanceScore"])
        ])
        return {"balanceAnalysis": ordered_balance_analysis}
    except json.JSONDecodeError:
        return {
            "balanceAnalysis": OrderedDict([
                ("simulationSummary", "분석 실패: 응답 형식 오류"),
                ("issuesDetected", []),
                ("recommendations", []),
                ("balanceScore", 0.0)
            ])
        }