from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class GameData:
    """게임 정보 데이터 클래스"""
    title: str
    theme: str
    mechanics: str
    description: str
    year: Optional[int] = None
    publisher: str = None
    source: str = "unknown"

@dataclass
class SimilarGame:
    """유사한 게임 정보"""
    title: str
    similarity_score: float
    risk_level: str
    data_source: str
    theme: str = ""
    mechanics: str = ""
    year: Optional[int] = None

@dataclass
class CopyrightCheckResponse:
    """저작권 검사 응답"""
    game_title: str
    decision: str  # "APPROVED" or "REJECTED"
    risk_level: str  # "minimal", "low", "medium", "high"
    max_similarity_score: float
    
    # 분석된 게임 요소들
    extracted_elements: Dict[str, str]
    
    # 유사 게임들
    similar_games: List[SimilarGame]
    
    # 권고사항
    recommendations: List[str]
    
    # 상세 정보
    total_games_checked: int
    data_sources_used: List[str]