import asyncio
from sqlalchemy import text
from core.database import engine, get_db, check_db_connection
from core.config import settings

def test_sync_connection():
    """동기 연결 테스트"""
    print("=== 동기 연결 테스트 ===")
    print(f"DB URL: {settings.db_url}")
    
    if check_db_connection():
        print("✅ 데이터베이스 연결 성공!")
        
        # 간단한 쿼리 실행
        try:
            with engine.connect() as conn:
                result = conn.execute(text("SELECT version()"))
                version = result.fetchone()
                print(f"PostgreSQL 버전: {version[0]}")
        except Exception as e:
            print(f"❌ 쿼리 실행 실패: {e}")
    else:
        print("❌ 데이터베이스 연결 실패!")

def test_session():
    """세션 테스트"""
    print("\n=== 세션 테스트 ===")
    try:
        db = next(get_db())
        result = db.execute(text("SELECT current_database()"))
        db_name = result.fetchone()
        print(f"✅ 현재 데이터베이스: {db_name[0]}")
        db.close()
    except Exception as e:
        print(f"❌ 세션 테스트 실패: {e}")

if __name__ == "__main__":
    test_sync_connection()
    test_session()