# app/google_file_search.py
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv

# Tải các biến môi trường từ tệp .env
load_dotenv()

# Lấy API key từ biến môi trường
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
CX = os.getenv("CX")

def search_google_file(query):
    # Khởi tạo Google API client với API key từ biến môi trường
    service = build("customsearch", "v1", developerKey=GEMINI_API_KEY)
    
    # Thực hiện truy vấn tìm kiếm
    res = service.cse().list(q=query, cx=CX).execute()
    return res['items']
