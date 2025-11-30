# frontend/app.py
import requests
import streamlit as st

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Library Rental", layout="wide")
st.title("📚 도서관 대여 시스템")


# ---------- Helpers ----------
def get_books():
    r = requests.get(f"{BACKEND_URL}/books")
    return r.json()


def get_active_loans():
    r = requests.get(f"{BACKEND_URL}/loans", params={"only_active": True})
    return r.json()

def get_all_loans():
    r = requests.get(f"{BACKEND_URL}/loans")  # không truyền only_active → lấy tất cả
    return r.json()



# ---------- UI ----------
menu = st.sidebar.radio(
    "Menu",
    ["도서 관리", "대여 / 반납", "대여 기록 조회"]
)


# ---------- Quản lý sách ----------
if menu == "도서 관리":
    st.subheader("📖 도서 추가")
    with st.form("add_book_form"):
        title = st.text_input("도서명")
        author = st.text_input("저자")
        total = st.number_input("총 권수", min_value=1, value=1, step=1)
        submitted = st.form_submit_button("추가")

    if submitted:
        payload = {"title": title, "author": author, "total_copies": total}
        r = requests.post(f"{BACKEND_URL}/books", json=payload)
        if r.status_code == 200:
            st.success("추가됨")
        else:
            st.error(f"오류: {r.text}")

    st.subheader("📚 도서 목록")
    books = get_books()

# 📌 Hiển thị bảng thông tin
    if books:
        st.table(
            [
                {
                    "ID": b["id"],
                    "제목": b["title"],
                    "저자": b["author"],
                    "총 권수": b["total_copies"],
                    "대여 가능 권수": b["available_copies"],
                }
                for b in books
            ]
        )
    else:
        st.info("도서가 없습니다.")

    # 📌 Khu vực xóa sách
    st.subheader("📌 도서 삭제")

    if books:
        for b in books:
            with st.expander(f"[{b['id']}] {b['title']} - {b['author']}"):
                st.write(f"총 권수: {b['total_copies']}")
                st.write(f"대여 가능 권수: {b['available_copies']}")

                if st.button("🗑 삭제하기", key=f"del_{b['id']}"):
                    r = requests.delete(f"{BACKEND_URL}/books/{b['id']}")
                    if r.status_code == 200:
                        st.success("도서를 삭제했습니다.")
                        st.rerun()   # 🔄 Refresh lại trang sau khi xóa
                    else:
                        try:
                            detail = r.json().get("detail", r.text)
                        except Exception:
                            detail = r.text
                        st.error(f"오류 발생: {detail}")




# ---------- Mượn / Trả sách ----------
elif menu == "대여 / 반납":
    st.subheader("📚 대여")
    books = get_books()
    if not books:
        st.warning("시스템에 등록된 도서가 없습니다.")

    else:
        # chỉ cho chọn sách còn bản
        options = [b for b in books if b["available_copies"] > 0]
        if not options:
            st.info("대여할 수 있는 도서가 없습니다.")

        else:
            book_titles = [
                f'{b["id"]} - {b["title"]} ({b["available_copies"]}권 남음)' 
                for b in options]
            choice = st.selectbox("대여할 도서 선택", book_titles)
            borrower = st.text_input("대여자 이름")


            if st.button("대여"):
                book_id = int(choice.split(" - ")[0])
                payload = {"book_id": book_id, "borrower_name": borrower}
                r = requests.post(f"{BACKEND_URL}/loans/borrow", json=payload)

                if r.status_code == 200:
                    st.success("도서 대여가 완료되었습니다.")
                else:
                    st.error(f"오류 발생: {r.text}")


    st.subheader("📄 대여 중인 도서 목록")
    active_loans = get_active_loans()

    if active_loans:
        for loan in active_loans:
            with st.expander(
                f'[{loan["id"]}] {loan["borrower_name"]} 님이 도서 ID {loan["book_id"]}을(를) 대여 중'
            ):
                st.write(loan)

                if st.button("반납", key=f"return_{loan['id']}"):
                    r = requests.post(f"{BACKEND_URL}/loans/{loan['id']}/return")

                    if r.status_code == 200:
                        st.success("반납이 완료되었습니다.")
                    else:
                        st.error(f"오류 발생: {r.text}")

# ---------- Lịch sử mượn / trả ----------
elif menu == "대여 기록 조회":
    st.subheader("📜 대여 / 반납 이력")

    loans = get_all_loans()
    if not loans:
        st.info("대여 / 반납 이력이 없습니다.")
    else:
        # 대여자 이름으로 필터링
        keyword = st.text_input("대여자 이름으로 검색 (선택)")

        if keyword:
            loans = [
                l for l in loans
                if keyword.lower() in l["borrower_name"].lower()
            ]

        # 테이블 형태로 표시
        table_data = []
        for l in loans:
            status = "반납 완료" if l["is_returned"] else "대여 중"
            return_date = l["return_date"] if l["return_date"] else "-"

            table_data.append(
                {
                    "대여 ID": l["id"],
                    "도서 ID": l["book_id"],
                    "대여자": l["borrower_name"],
                    "대여일": l["borrow_date"],
                    "반납일": return_date,
                    "상태": status,
                }
            )

        st.table(table_data)
