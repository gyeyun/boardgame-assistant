import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db.db_connector import SessionLocal
from models.rulebook import Rulebook
from datetime import datetime

db = SessionLocal()

rulebook = Rulebook(
    plan_id=1,
    rule_set="""
1. 게임 개요
플레이어들은 궁정 연금술사 자리를 두고 경쟁하며 약초, 광물 등을 수집하고 정수를 생산해 칙령을 수행하는 전략 게임입니다.

2. 게임 목표
7라운드 동안 명성 점수를 가장 많이 획득한 플레이어가 승리합니다.

3. 구성 요소
- 장치 카드, 칙령 카드, 포션 카드 등
- 정수 토큰, 점수 마커, 개인 보드 등

4. 게임 진행
- 드래프팅 → 엔진 가동 → 계약 납품 → 정리 순으로 7라운드 진행

5. 승리 조건
- 명성 점수를 가장 많이 획득한 플레이어가 승리
""",
    win_condition="명성 점수를 가장 많이 획득한 플레이어가 승리",
    turn_order="시계 방향으로 진행",
    created_at=datetime.now()
)

db.add(rulebook)
db.commit()
db.close()
print("✅ 샘플 Rulebook 삽입 완료")
