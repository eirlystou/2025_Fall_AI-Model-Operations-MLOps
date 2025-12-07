# app.py
import streamlit as st
import requests

# Cấu hình URL API FastAPI
API_URL = "http://localhost:8000/search/"

# Tiêu đề giao diện
st.title("Google Gemini API Search")

# Form nhập truy vấn tìm kiếm
query = st.text_input("Enter your search query:")

# Nút tìm kiếm
if st.button("Search"):
    if query:
        # Gửi truy vấn tìm kiếm đến FastAPI
        response = requests.get(API_URL, params={"query": query})
        
        # Kiểm tra phản hồi từ API
        if response.status_code == 200:
            data = response.json()
            
            # Hiển thị kết quả tìm kiếm
            if "google_results" in data:
                st.write(f"Found {len(data['google_results'])} result(s):")
                for item in data["google_results"]:
                    st.write(f"**{item['title']}**")
                    st.write(f"Link: {item['link']}")
                    st.write(f"{item['snippet']}")
            else:
                st.write("No results found.")
        else:
            st.write("Error in fetching data from API.")
    else:
        st.write("Please enter a search query.")
