# Rulebook - 룰북 내용 생성

## 기능 설명
- 룰북 내용을 기확안을 바탕으로 생성

## 구현할 항목
- [ ] plan 기반 설명 요약 생성
- [ ] /api/content/generate-rulebook-script API 구현

기획안 plan 으로 불러옴 -> 수정 해야함


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
