#룰북 생성 LLM 호출 함수
from utils.openai_utils import call_openai

def generate_rulebook_from_prompt(prompt: str):
    full_prompt = f"""
너는 전문 보드게임 디자이너야.
다음 기획안을 바탕으로 보드게임의 룰북을 작성해줘.

기획안:
{prompt}

룰북은 다음 9개의 항목으로 구성되어야 해:

1. 게임 제목  
2. 게임 소개 (스토리, 테마, 장르 중심으로 5~6줄 분량의 설명)  
3. 구성품 (형식: "구성품 이름 X 개수"로 나열)  
4. 적정 연령  
5. 게임 준비 (보드 세팅, 플레이어 준비물 등 상세히)  
6. 게임 규칙 (플레이 순서, 행동, 제약 조건 등 세부 규칙 설명)  
7. 게임 진행 방식 (턴이 흐르는 구조, 라운드 방식 등)  
8. 승리 조건 (누가 언제 어떻게 이기는지 구체적으로)  
9. 턴 순서 (플레이어가 어떤 순서로 행동하는지 명확하게)

각 항목은 번호와 제목을 붙여서 출력해줘.
서술은 자연스럽고 일관성 있게 써줘.
"""
    response = call_openai(full_prompt)

    # 예시 파싱 로직 (단순 정규 표현식/구분자 사용 가능)
    rule_set = extract_section(response, "게임 규칙")
    win_condition = extract_section(response, "승리 조건")
    turn_order = extract_section(response, "턴 순서")
    return rule_set, win_condition, turn_order

def extract_section(text: str, title: str) -> str:
    # 간단한 추출 로직: "## 제목" 같은 구분을 기준으로 자를 수 있음
    import re
    pattern = f"{title}[^\n]*\n(.*?)(\n#|$)"
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1).strip() if match else ""
