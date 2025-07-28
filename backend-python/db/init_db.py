from db.db_connector import Base, engine
from models import user, role, project, plan, concept, rulebook, content 

Base.metadata.create_all(bind=engine)
print("✅ 데이터베이스 테이블 생성 완료")