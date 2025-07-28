from analyzer import GamePlanAnalyzer
from checker import SimilarityChecker
from judge import CopyrightJudge
from schema import GameData, SimilarGame, CopyrightCheckResponse

class CopyrightCheckService:
    """저작권 검사 서비스 - 전체 프로세스 통합"""
    
    def __init__(self):
        self.analyzer = GamePlanAnalyzer()
        self.checker = SimilarityChecker()
        self.judge = CopyrightJudge()
    
    def check_copyright(self, game_plan: str, plan_title: str) -> CopyrightCheckResponse:
        """전체 저작권 검사 프로세스 실행"""
        
        print("="*60)
        print(f"🎲 보드게임 저작권 검사 시작: '{plan_title}'")
        print("="*60)
        
        # 1단계: 기획서 분석
        game_data = self.analyzer.extract_game_elements(game_plan, plan_title)
        
        # 2단계: 유사도 검사
        similar_games_data = self.checker.search_similar_games(game_data)
        
        # 3단계: 위험도 판정
        print("3단계: 최종 판정 중...")
        max_similarity = similar_games_data[0]['similarity'] if similar_games_data else 0.0
        risk_level = self.judge.determine_risk_level(max_similarity)
        decision = self.judge.make_decision(risk_level, max_similarity)
        
        # 4단계: 응답 생성
        print("4단계: 결과 리포트 생성 중...")
        
        # SimilarGame 객체들 생성
        similar_games = []
        for game_info in similar_games_data:
            similar_games.append(SimilarGame(
                title=game_info['title'],
                similarity_score=game_info['similarity'],
                risk_level=self.judge.determine_risk_level(game_info['similarity']),
                data_source="BGG",
                theme=game_info.get('theme', ''),
                mechanics=game_info.get('mechanics', ''),
                year=game_info.get('year')
            ))
        
        # 권고사항 생성
        recommendations = self.judge.generate_recommendations(
            risk_level, decision, similar_games_data, max_similarity
        )
        
        # 최종 응답 생성
        response = CopyrightCheckResponse(
            game_title=game_data.title,
            decision=decision,
            risk_level=risk_level,
            max_similarity_score=max_similarity,
            extracted_elements={
                "theme": game_data.theme,
                "mechanics": game_data.mechanics,
                "description": game_data.description
            },
            similar_games=similar_games,
            recommendations=recommendations,
            total_games_checked=len(similar_games_data),
            data_sources_used=["BGG"]
        )
        
        print("✅ 저작권 검사 완료!")
        return response