import re
import json
from typing import List, Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from bgg_utils import BGGAPIClient
from openai_utils import call_openai
from schema import GameData

class SimilarityChecker:
    """향상된 게임 유사도 검사기 - OpenAI 통합"""
    
    def __init__(self):
        self.bgg_client = BGGAPIClient(request_delay=2.0)
        self.vectorizer = TfidfVectorizer(
            stop_words='english', 
            ngram_range=(1, 2),
            max_features=1000
        )
    
    def generate_smart_search_terms(self, new_game: GameData) -> List[str]:
        """OpenAI를 사용해 더 효과적인 BGG 검색어 생성 + 직접 게임명 검색"""
        
        prompt = f"""
다음 게임 정보를 바탕으로 BoardGameGeek에서 유사한 게임을 찾기 위한 
최적의 검색어들을 생성해주세요.

게임 정보:
- 제목: {new_game.title}
- 테마: {new_game.theme}  
- 메커닉: {new_game.mechanics}
- 설명: {new_game.description}

요구사항:
1. BGG에서 실제로 검색 가능한 영어 키워드들
2. 이 게임과 유사한 기존 게임들을 찾을 수 있는 검색어
3. 유명한 게임명도 포함 (예: splendor, catan, wingspan 등)
4. 5-8개의 검색어를 JSON 배열로 반환

JSON 형태로만 답변해주세요:
"""
        
        try:
            response = call_openai(prompt, max_tokens=200, temperature=0.3)
            
            # JSON 파싱
            json_start = response.find('[')
            json_end = response.rfind(']') + 1
            
            if json_start != -1 and json_end > json_start:
                json_text = response[json_start:json_end]
                search_terms = json.loads(json_text)
            else:
                search_terms = self._fallback_search_terms(new_game)
            
            # 추가 직접 게임명 검색어
            popular_games = self._get_popular_game_names(new_game)
            search_terms.extend(popular_games)
            
            # 중복 제거
            search_terms = list(dict.fromkeys(search_terms))
            
            print(f"    생성된 검색어: {search_terms[:10]}")
            return search_terms[:10]  # 최대 10개로 제한
            
        except Exception as e:
            print(f"    검색어 생성 실패, 기본 방식 사용: {e}")
            return self._fallback_search_terms(new_game)
    
    def _get_popular_game_names(self, new_game: GameData) -> List[str]:
        """메커닉/테마 기반으로 유명 게임명 추가"""
        popular_games = []
        
        mechanics_lower = new_game.mechanics.lower()
        theme_lower = new_game.theme.lower()
        desc_lower = new_game.description.lower()
        
        # 엔진 빌딩 관련
        if any(keyword in mechanics_lower for keyword in ['engine', 'card', 'discount', 'permanent']):
            popular_games.extend(['splendor', 'wingspan', 'gizmos'])
        
        # 자원 관리 + 건설 관련
        if any(keyword in mechanics_lower for keyword in ['resource', 'build', 'settlement', 'trade', 'dice']):
            popular_games.extend(['catan', 'settlers of catan', 'chinatown'])
        
        # 덱빌딩 관련
        if any(keyword in mechanics_lower for keyword in ['deck', 'dominion', 'card']):
            popular_games.extend(['dominion', 'ascension', 'star realms'])
        
        # 워커 플레이스먼트 관련
        if any(keyword in mechanics_lower for keyword in ['worker', 'placement', 'action']):
            popular_games.extend(['agricola', 'lords of waterdeep', 'stone age'])
        
        # 자연/동물 테마
        if any(keyword in theme_lower for keyword in ['bird', 'animal', 'nature', 'wildlife']):
            popular_games.extend(['wingspan', 'evolution', 'ark nova'])
        
        return popular_games
    
    def _fallback_search_terms(self, new_game: GameData) -> List[str]:
        """백업용 검색어 생성"""
        terms = []
        if new_game.theme:
            terms.extend(new_game.theme.split()[:3])
        if new_game.mechanics:
            terms.extend(new_game.mechanics.split()[:3])
        return [term for term in terms if len(term) > 2]
    
    def intelligent_similarity_analysis(self, new_game: GameData, bgg_games: List) -> List[Dict]:
        """OpenAI를 사용한 지능적 유사도 분석"""
        
        if not bgg_games:
            return []
        
        # BGG 게임들을 텍스트로 변환
        bgg_summaries = []
        for game in bgg_games:
            summary = f"""
Title: {game.title} ({game.year if game.year else 'Unknown'})
Categories: {', '.join(game.categories[:3]) if game.categories else 'None'}
Mechanics: {', '.join(game.mechanics[:3]) if game.mechanics else 'None'}  
Description: {game.description[:200] if game.description else 'No description'}
"""
            bgg_summaries.append(summary.strip())
        
        prompt = f"""
다음 새 게임과 기존 게임들 간의 유사도를 전문적으로 분석해주세요.

새 게임:
제목: {new_game.title}
테마: {new_game.theme}
메커닉: {new_game.mechanics}
설명: {new_game.description}

기존 게임들:
{chr(10).join(f"{i+1}. {summary}" for i, summary in enumerate(bgg_summaries))}

각 기존 게임과 새 게임의 유사도를 다음 기준으로 평가해주세요:

1. 핵심 게임 메커닉의 유사성 (50%) - 가장 중요
   - 자원 수집/관리 방식
   - 승리 조건과 점수 시스템
   - 플레이어 상호작용 방식
   - 게임 진행 구조

2. 테마/세팅의 유사성 (25%)
   - 배경 스토리와 분위기
   - 컴포넌트의 주제적 연관성

3. 게임 경험의 유사성 (25%)
   - 플레이 시간과 복잡도
   - 전략적 깊이와 선택의 폭

특별 주의사항:
- 단순한 키워드 매칭이 아닌 실제 게임플레이 구조 비교
- 유명 게임(Splendor, Catan, Wingspan 등)과의 비교 시 더 엄격하게 평가
- 메커닉의 조합이 독창적인지 고려

결과를 다음 JSON 형태로 반환해주세요:
[
  {{
    "game_index": 0,
    "similarity_score": 0.85,
    "risk_assessment": "high",
    "reasoning": "핵심 메커닉과 승리 조건이 매우 유사함. 특히 X 게임의 Y 메커닉과 거의 동일"
  }},
  ...
]

유사도 점수 기준:
- 0.0-0.3: 다른 게임 (테마만 유사하거나 일반적 메커닉)
- 0.3-0.6: 약간 유사 (일부 메커닉 공통점)
- 0.6-0.8: 상당히 유사 (핵심 메커닉 유사, 주의 필요)
- 0.8-1.0: 매우 유사 (게임 구조 거의 동일, 저작권 위험)
"""
        
        try:
            print(f"    OpenAI로 {len(bgg_games)}개 게임과 유사도 분석 중...")
            response = call_openai(prompt, max_tokens=1500, temperature=0.2)
            
            # JSON 파싱
            json_start = response.find('[')
            json_end = response.rfind(']') + 1
            
            if json_start != -1 and json_end > json_start:
                json_text = response[json_start:json_end]
                analysis_results = json.loads(json_text)
                
                # 결과를 기존 형태로 변환
                similar_games = []
                for result in analysis_results:
                    if result['game_index'] < len(bgg_games):
                        game = bgg_games[result['game_index']]
                        similar_games.append({
                            'title': game.title,
                            'similarity': result['similarity_score'],
                            'theme': ', '.join(game.categories[:3]) if game.categories else '',
                            'mechanics': ', '.join(game.mechanics[:3]) if game.mechanics else '',
                            'year': game.year,
                            'description': game.description,
                            'reasoning': result.get('reasoning', '')
                        })
                
                print(f"    ✓ OpenAI 분석 완료: {len(similar_games)}개 게임")
                return sorted(similar_games, key=lambda x: x['similarity'], reverse=True)
            
        except Exception as e:
            print(f"    OpenAI 분석 실패, 기존 방식으로 폴백: {e}")
        
        # 실패 시 기존 TF-IDF 방식으로 폴백
        return self._fallback_similarity_calculation(new_game, bgg_games)
    
    def _fallback_similarity_calculation(self, new_game: GameData, bgg_games: List) -> List[Dict]:
        """기존 TF-IDF 방식 (백업용)"""
        similar_games = []
        
        for bgg_game in bgg_games:
            theme_text = " ".join(bgg_game.categories or [])
            mechanics_text = " ".join(bgg_game.mechanics or [])
            
            theme_sim = self._calculate_tfidf_similarity(new_game.theme, theme_text)
            mechanics_sim = self._calculate_tfidf_similarity(new_game.mechanics, mechanics_text)
            desc_sim = self._calculate_tfidf_similarity(new_game.description, bgg_game.description)
            
            overall_sim = theme_sim * 0.3 + mechanics_sim * 0.4 + desc_sim * 0.3
            
            if overall_sim > 0.1:
                similar_games.append({
                    'title': bgg_game.title,
                    'similarity': overall_sim,
                    'theme': theme_text,
                    'mechanics': mechanics_text,
                    'year': bgg_game.year,
                    'description': bgg_game.description
                })
        
        return sorted(similar_games, key=lambda x: x['similarity'], reverse=True)
    
    def _calculate_tfidf_similarity(self, text1: str, text2: str) -> float:
        """TF-IDF 코사인 유사도 계산"""
        try:
            if not text1 or not text2:
                return 0.0
            
            texts = [text1.lower(), text2.lower()]
            tfidf_matrix = self.vectorizer.fit_transform(texts)
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return float(similarity)
        except:
            return 0.0
    
    def search_similar_games(self, new_game: GameData) -> List[Dict]:
        """향상된 유사 게임 검색"""
        print(f"2단계: '{new_game.title}' 향상된 유사도 검사 시작...")
        
        # 1. 스마트 검색어 생성
        search_terms = self.generate_smart_search_terms(new_game)
        
        # 2. BGG에서 게임 검색
        all_bgg_games = []
        seen_titles = set()
        
        for term in search_terms:
            try:
                game_ids = self.bgg_client.search_games(term, max_results=5)
                if game_ids:
                    bgg_games = self.bgg_client.get_game_details(game_ids)
                    
                    for game in bgg_games:
                        if game.title not in seen_titles:
                            seen_titles.add(game.title)
                            all_bgg_games.append(game)
                            
            except Exception as e:
                print(f"  검색어 '{term}' 처리 중 오류: {e}")
                continue
        
        # 3. OpenAI로 지능적 유사도 분석
        similar_games = self.intelligent_similarity_analysis(new_game, all_bgg_games)
        
        print(f"  ✓ 총 {len(similar_games)}개 유사 게임 발견")
        return similar_games[:10]