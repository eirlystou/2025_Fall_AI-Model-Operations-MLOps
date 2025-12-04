import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Tiêu đề cho dashboard (tiếng Hàn)
st.title("🎶 Chinook 음악 대시보드")

# Sidebar với các lựa chọn radio (tiếng Hàn)
selection = st.sidebar.radio(
    "보고 싶은 통계를 선택하세요:",  # "Chọn loại thống kê bạn muốn xem:"
    ("각 아티스트의 앨범 수",  # "Số lượng album của mỗi nghệ sĩ"
     "각 앨범의 트랙 수",  # "Số lượng bài hát trong mỗi album"
     "각 플레이리스트의 트랙 수",  # "Số lượng bài hát trong mỗi playlist"
     "트랙 수 기준 상위 아티스트")  # "Nghệ sĩ hàng đầu dựa trên số lượng bài hát"
)

# Lấy dữ liệu từ API
def fetch_data_from_api(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"{url}에서 데이터를 가져오는 중 오류가 발생했습니다. 오류 코드: {response.status_code}")
        return None

# Lấy số lượng album của mỗi nghệ sĩ từ API
def get_album_count_data():
    url = "http://127.0.0.1:8000/album_count/10"
    return fetch_data_from_api(url)

# Lấy số lượng bài hát trong mỗi album từ API
def get_track_count_in_album_data():
    url = "http://127.0.0.1:8000/track_count_in_album/10"
    return fetch_data_from_api(url)

# Lấy số lượng bài hát trong mỗi playlist từ API
def get_track_count_in_playlist_data():
    url = "http://127.0.0.1:8000/track_count_in_playlist/10"
    return fetch_data_from_api(url)

# Lấy dữ liệu nghệ sĩ hàng đầu dựa trên số lượng bài hát
def get_top_artists_data(limit):
    url = f"http://127.0.0.1:8000/top_artists/{limit}"
    return fetch_data_from_api(url)

# Hiển thị kết quả tùy thuộc vào lựa chọn của người dùng
if selection == "각 아티스트의 앨범 수":  # "Số lượng album của mỗi nghệ sĩ"
    album_data = get_album_count_data()
    if album_data:
        df_album = pd.DataFrame(album_data["data"], columns=["ArtistName", "AlbumCount"])
        st.subheader("각 아티스트의 앨범 수:")
        st.dataframe(df_album)

        # Biểu đồ tròn (pie chart)
        fig_album = px.pie(df_album, names='ArtistName', values='AlbumCount', title="각 아티스트의 앨범 수")
        st.plotly_chart(fig_album)

elif selection == "각 앨범의 트랙 수":  # "Số lượng bài hát trong mỗi album"
    track_album_data = get_track_count_in_album_data()
    if track_album_data:
        df_track_album = pd.DataFrame(track_album_data["data"], columns=["AlbumTitle", "TrackCount"])
        st.subheader("각 앨범의 트랙 수:")
        st.dataframe(df_track_album)

        # Biểu đồ đường (line chart)
        fig_track_album = px.line(df_track_album, x='AlbumTitle', y='TrackCount', title="각 앨범의 트랙 수", markers=True)
        st.plotly_chart(fig_track_album)

elif selection == "각 플레이리스트의 트랙 수":  # "Số lượng bài hát trong mỗi playlist"
    track_playlist_data = get_track_count_in_playlist_data()
    if track_playlist_data:
        df_track_playlist = pd.DataFrame(track_playlist_data["data"], columns=["PlaylistName", "TrackCount"])
        st.subheader("각 플레이리스트의 트랙 수:")
        st.dataframe(df_track_playlist)

        # Biểu đồ vùng (area chart)
        fig_track_playlist = px.area(df_track_playlist, x='PlaylistName', y='TrackCount', title="각 플레이리스트의 트랙 수")
        st.plotly_chart(fig_track_playlist)

elif selection == "트랙 수 기준 상위 아티스트":  # "Nghệ sĩ hàng đầu dựa trên số lượng bài hát"
    top_artists_data = get_top_artists_data(10)
    if top_artists_data:
        df_top_artists = pd.DataFrame(top_artists_data, columns=["ArtistName", "TrackCount"])
        st.subheader("트랙 수 기준 상위 아티스트:")
        st.dataframe(df_top_artists)

        # Biểu đồ cột (bar chart)
        fig_top_artists = px.bar(df_top_artists, x='ArtistName', y='TrackCount', title="트랙 수 기준 상위 아티스트", color='ArtistName')
        st.plotly_chart(fig_top_artists)
