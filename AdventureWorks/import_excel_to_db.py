# -*- coding: utf-8 -*-
import pandas as pd
import sqlite3
import os

# --- 설정 ---
# 엑셀 파일이 포함된 디렉토리 경로
DATA_DIR = 'data'

# 원본 엑셀 파일 이름
EXCEL_FILENAME = 'AdventureWorks-Sales.xlsx' # <-- 엑셀 파일을 'data/' 폴더에 넣어주세요.

# 생성할 SQLite 파일 경로
DB_PATH = os.path.join(DATA_DIR, 'AdventureWorks-Sales.sqlite3')

# 엑셀 시트 이름을 DB 테이블 이름으로 매핑
#
# 엑셀 파일을 열어 실제 시트 이름을 확인하고 수정해야 합니다.
#
SHEETS_TO_IMPORT = {
    'Reseller_data': 'Resellers',
    'Sales_data': 'Sales',
    'Customer_data': 'Customers',
    'Product_data': 'Products',
    'Sales Territory_data': 'Territories',
    'Sales Order_data': 'SalesOrder',
    'Date_data': 'Date'
}
# --- 설정 끝 ---

def import_excel_to_sqlite():
    """
    하나의 엑셀 파일에서 여러 시트를 읽어 
    하나의 SQLite 데이터베이스 파일에 테이블로 저장합니다.
    """
    
    excel_file_path = os.path.join(DATA_DIR, EXCEL_FILENAME)
    
    # 1. 엑셀 파일 확인
    if not os.path.exists(excel_file_path):
        print(f"오류: '{excel_file_path}'에서 엑셀 파일을 찾을 수 없습니다.")
        print("'AdventureWorks-Sales.xlsx' 파일을 'data' 디렉토리에 다운로드하세요.")
        return

    # 2. 기존 DB 파일이 있으면 삭제 (새로 만들기 위해)
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"기존 데이터베이스 파일 삭제: {DB_PATH}")

    conn = None
    try:
        # 3. 새 DB에 연결 생성
        conn = sqlite3.connect(DB_PATH)
        print(f"새 데이터베이스 파일 생성: {DB_PATH}")

        # 4. 엑셀 파일 읽기
        print(f"엑셀 파일 읽는 중: {excel_file_path}...")
        xls = pd.ExcelFile(excel_file_path)

        # 5. 시트를 반복하며 가져오기
        total_sheets = len(SHEETS_TO_IMPORT)
        count = 0
        for sheet_name, table_name in SHEETS_TO_IMPORT.items():
            count += 1
            print(f"[{count}/{total_sheets}] 시트 처리 중: '{sheet_name}'...")
            
            try:
                # 시트를 DataFrame으로 읽기
                df = pd.read_excel(xls, sheet_name=sheet_name)
                
                # DataFrame을 SQLite 테이블로 저장
                df.to_sql(table_name, conn, index=False, if_exists='replace')
                
                print(f" -> '{table_name}' 테이블로 가져오기 성공")
                
            except ValueError:
                print(f" 오류: 엑셀 파일에서 '{sheet_name}' 시트를 찾을 수 없습니다.")
                print(" -> 'SHEETS_TO_IMPORT' 설정을 다시 확인하세요.")
            except Exception as e:
                print(f" 오류: '{table_name}' 테이블 가져오기 실패: {e}")

        print(f"\n완료! '{DB_PATH}' 파일이 생성되었습니다.")

    except Exception as e:
        print(f"전체 오류 발생: {e}")
    finally:
        if conn:
            conn.close()
            print("데이터베이스 연결 종료.")

if __name__ == "__main__":
    import_excel_to_sqlite()