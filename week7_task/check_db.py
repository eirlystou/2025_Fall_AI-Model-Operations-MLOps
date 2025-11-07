# -*- coding: utf-8 -*-
import sqlite3
import os

DB_PATH = os.path.join('data', 'AdventureWorks-Sales.sqlite3') 

def list_tables(db_file):
    """데이터베이스에 연결하고 모든 테이블을 인쇄합니다."""
    
    # 1. 파일이 존재하는지 확인
    if not os.path.exists(db_file):
        print(f"오류: '{db_file}'에서 데이터베이스 파일을 찾을 수 없습니다.")
        print("파일을 다운로드하여 올바른 'data/' 디렉토리에 배치했는지 확인하세요.")
        return

    conn = None
    try:
        # 2. 연결 생성
        conn = sqlite3.connect(db_file)
        
        # 3. 커서 생성
        cursor = conn.cursor()
        
        # 4. SQL 명령을 실행하여 테이블 이름 가져오기
        # 'sqlite_master'는 메타데이터를 포함하는 특수 시스템 테이블입니다.
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        
        # 5. 모든 결과 가져오기
        tables = cursor.fetchall()
        
        if not tables:
            print(f"데이터베이스 '{db_file}'에 테이블이 없습니다.")
        else:
            print(f"--- '{db_file}'에 있는 테이블 ---")
            for table in tables:
                print(f"- {table[0]}") # 결과는 튜플로 반환됩니다 (예: ('Sales',))

    except sqlite3.Error as e:
        print(f"SQLite 오류 발생: {e}")
    except Exception as e:
        print(f"오류 발생: {e}")
    finally:
        # 6. 연결 닫기
        if conn:
            conn.close()

if __name__ == "__main__":
    list_tables(DB_PATH)