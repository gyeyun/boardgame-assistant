import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def evaluate_balance(game_data: dict) -> str:
    prompt = f"""
    당신은 전문 보드게임 디자이너이자 시뮬레이션 설계자입니다.

    다음은 보드게임의 구성 요소입니다:

    - 난이도: {game_data["difficulty"]}
    - 인원: {game_data["player_count"]}
    - 주요 목표: {', '.join(game_data["main_objectives"])}
    - 행동 규칙: {', '.join(game_data["rules"])}
    - 승리 조건: {', '.join(game_data["win_conditions"])}
    - 패배/탈락 조건: {', '.join(game_data["fail_conditions"])}

    이제 당신은 **이 게임을 머릿속으로 직접 시뮬레이션**해 보며 다음을 평가해야 합니다.

    1. **게임 밸런스 평가**  
       - 난이도, 반복성, 플레이 전략 다양성 등을 고려해 평가하세요.

    2. **시뮬레이션 평가 (종료 여부 포함)**  
       - 실제 이 규칙대로 게임이 실행되면 반드시 종료되는 구조인가요?  
       - 특정 요소 때문에 **게임이 절대 끝나지 않는 구조**는 아닌가요?  
       - '승리 조건이 이론적으로 달성 불가능'하거나 '패배 조건이 현실적으로 발생하지 않는 경우'가 있나요?  
       - 이러한 경우, **무한 루프가 발생하는 이유**를 명확히 설명하세요.

    3. **누락된 요소 및 개선 제안**  
       - 재미, 다양성, 리플레이성 향상을 위한 요소나 밸런스 수정을 제안하세요.

    아래 형식으로 작성하세요:

    - 밸런스 평가:
    - 시뮬레이션 평가:
    - 누락된 요소 (있다면):
    - 개선 제안:
    """

    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )

    return chat_completion.choices[0].message.content
