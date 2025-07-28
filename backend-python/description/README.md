# Description - 설명 스크립트 생성

## 기능 설명
- 룰북 또는 게임 소개 스크립트 자동 생성

## 구현할 항목
- [ ] rulebook 기반 설명 요약 생성
- [ ] /api/content/generate-description-script API 구현

python -m venv venv
가상환경 활성화
source venv/bin/activate

pip install sqlalchemy pymysql
pip install python-dotenv
pip install fastapi[all]
pip install openai
pip install sqlalchemy
pip install sqlalchemy openai python-dotenv pymysql


FastAPI 서버 실행
PYTHONPATH=./backend-python uvicorn app:app --reload


MariaDB 백그라운드 실행
docker run -d \
  --name mariadb \
  -e MYSQL_ROOT_PASSWORD=123123d \
  -e MYSQL_DATABASE=boardgame \
  -p 3306:3306 \
  mariadb


plan_id, project_id 생성된 설명 스크립트를 description 유형으로 DB(Content 또는 Description)에 저장할 때 사용됩니다.
rulebook_id         Rulebook 테이블에서 해당 ID의 룰북 데이터를 조회합니다.
룰북 데이터로 설명 스크립트 생성




backend-python/
    nit_db.py	DB 테이블 생성용 초기화 스크립트 (SQLAlchemy 기반) #######테스트용 임시 룰북 데이터를 Rulebook 테이블에 삽입
    insert_sample_rulebook.py	테스트용 룰북 데이터를 Rulebook 테이블에 삽입 ######테스트용  DB 테이블을 초기 생성
    app.py	FastAPI 앱 실행 진입점. 라우터를 포함하여 실행

backend-python/description/
    description_api.py	설명 스크립트 생성 및 저장 API 라우터 (POST /api/content/generate-description-script) GET /api/content도 포함되어 있음
    description_generator.py	OpenAI를 호출해 설명 스크립트를 생성하는 함수 (generate_description_script) 정의

backend-python/models/
    rulebook.py	    Rulebook 테이블 모델 정의 (rulebook_id, rulebook_set, win_condition, turn_order)
    content.py	Content 테이블 모델 정의 (plan_id, project_id, contentType, data, created_at, ...)


backend-python/db/
    db_connector.py	    SQLAlchemy DB 연결 설정 및 SessionLocal, Base 정의 .env의 DATABASE_URL 사용

backend-python/utils/
    openai_utils.py	   call_openai(prompt) 함수 정의 OpenAI API를 사용해 채팅 응답 생성




    Content 테이블 contentType 필드에 "description_script" 저장

    예시   {
    "script": "[장면: 보드게임 테이블 위]\n\n(카메라가 보드게임 테이블을 비추며 배경 음악이 감미롭게 흐르는 중)\n\n앵커:\n안녕하세요, 여러분! 오늘은 새로운 보드게임 '시대를 넘어'를 소개해 드리려고 합니다. 이 게임은 역사와 전략을 결합한 혁신적인 게임으로, 플레이어는 다양한 시대를 넘나들며 자원을 수집하고 발전시켜가는 재미있는 경쟁을 즐길 수 있습니다.\n\n(화면이 보드게임 상황을 보여주며 설명이 이어짐)\n\n앵커:\n이 게임은 2~4명의 플레이어가 참여할 수 있으며, 각 플레이어는 시대 카드, 자원 카드, 건물 카드, 그리고 기술 카드를 활용해 전략을 세우게 됩니다.\n\n(화면이 게임 컴포넌트들을 보여주며 설명이 이어짐)\n\n앵커:\n게임은 시대마다 다양한 목표를 달성하고 자원을 획득하여 건물을 건설하거나 기술을 개발합니다. 또한, 다른 플레이어와 거래를 통해 협력하거나 경쟁할 수도 있답니다.\n\n(화면이 게임 플레이 과정을 보여주며 설명이 이어짐)\n\n앵커:\n각 시대의 종료마다 플레이어는 목표를 달성하거나 행동을 통해 점수를 얻게 되는데요. 시대를 넘어가면서 어떤 전략을 펼칠지, 어떤 선택을 할지가 승부요소가 됩니다.\n\n(화면이 게임 플레이어들의 리액션을 보여주며 설명이 이어짐)\n\n앵커:\n게임은 모든 시대가 종료되면 최종 점수를 확인하여 가장 높은 점수를 획득한 플레이어가 승리하게 됩니다. 그리고 게임의 턴 순서는 시계 방향으로 진행되니 주의하세요!\n\n(화면이 게임 종료 상황을 보여주며 설명이 이어짐)\n\n앵커:\n'시대를 넘어'는 역사와 전략을 결합한 흥미진진한 보드게임으로, 친구들과 함께 시대를 넘나들며 승부를 겨루어보세요. 여러분도 함께 즐겁게 플레이해 보세요!\n\n(화면이 보드게임 테이블 위에서 전체적인 게임 컴포넌트를 보여주며 영상이 마무리됨)\n\n앵커:\n이상으로 '시대를 넘어' 게임 소개였습니다. 즐거운 보드게임 타임 되세요! 감사합니다.\n\n(화면이 서서히 어두워지며 영상이 끝나는 장면)"
  }