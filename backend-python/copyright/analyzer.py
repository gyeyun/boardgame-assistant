import json
from openai_utils import call_openai
from schema import GameData

class GamePlanAnalyzer:
    """게임 기획서 AI 분석기"""
    
    def extract_game_elements(self, game_plan: str, plan_title: str) -> GameData:
        """기획서에서 저작권 검사에 필요한 핵심 요소 추출"""
        
        prompt = f"""
다음 보드게임 기획서를 분석하여 저작권 검사에 필요한 핵심 요소들을 추출해주세요.

게임 제목: {plan_title}

기획서 내용:
{game_plan}

아래 JSON 형태로 정확히 반환해주세요. 다른 설명 없이 JSON만 반환하세요:

{{
  "title": "게임의 실제 제목",
  "theme": "게임의 주요 테마 키워드들 (예: horror mansion exploration, space colony building, medieval fantasy war)",
  "mechanics": "핵심 게임 메커닉 키워드들 (예: cooperative hidden traitor, deck building resource management, tile placement voting)",
  "description": "게임의 핵심 컨셉과 플레이 방식을 3문장 이내로 요약"
}}

중요: 
- theme과 mechanics는 영어 키워드로 작성 (BGG 검색용)
- 저작권 검사에 중요한 독창적 요소들을 정확히 추출
- JSON 형식을 정확히 지켜주세요
"""
        
        try:
            print(f"1단계: '{plan_title}' 기획서 분석 중...")
            response = call_openai(prompt)
            
            # JSON 추출
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            
            if json_start == -1:
                raise ValueError("JSON을 찾을 수 없습니다")
            
            json_text = response[json_start:json_end]
            parsed = json.loads(json_text)
            
            game_data = GameData(
                title=parsed.get('title', plan_title),
                theme=parsed.get('theme', ''),
                mechanics=parsed.get('mechanics', ''),
                description=parsed.get('description', ''),
                source="User Input"
            )
            
            print(f"  ✓ 추출 완료 - 테마: {game_data.theme}")
            print(f"  ✓ 메커닉: {game_data.mechanics}")
            return game_data
            
        except Exception as e:
            print(f"  ✗ 기획서 분석 오류: {e}")
            return GameData(
                title=plan_title,
                theme="analysis failed",
                mechanics="analysis failed",
                description=game_plan[:200] + "..." if len(game_plan) > 200 else game_plan,
                source="User Input"
            )