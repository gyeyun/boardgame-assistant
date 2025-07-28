from db.db_connector import engine, Base
from models.project import Project  
from models.plan import Plan
from models.rulebook import Rulebook
from models.content import Content

Base.metadata.create_all(bind=engine)
print("✅ 데이터베이스 테이블 생성 완료")