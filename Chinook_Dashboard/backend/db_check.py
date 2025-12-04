import sqlite3

# Kết nối với cơ sở dữ liệu SQLite
conn = sqlite3.connect('Chinook_Sqlite.sqlite')
cursor = conn.cursor()

# Thực thi câu truy vấn để lấy tất cả tên bảng
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

# Lấy kết quả và in ra các bảng
tables = cursor.fetchall()
print("Các bảng trong cơ sở dữ liệu:", tables)

cursor.execute("SELECT * FROM Track LIMIT 5;")
rows = cursor.fetchall()
print("5 dòng đầu tiên trong bảng Track:")

cursor.execute("SELECT COUNT(*) FROM Track;")
count = cursor.fetchone()[0]
print("Tổng số bản ghi trong bảng Track:", count)

cursor.execute("PRAGMA table_info(Track);")
columns = cursor.fetchall()
print("Thông tin cột của bảng Track:", columns)

cursor.execute("PRAGMA table_info(Artist);")
columns = cursor.fetchall()
print("Thông tin cột của bảng Artist:", columns)



# Đóng kết nối
conn.close()
