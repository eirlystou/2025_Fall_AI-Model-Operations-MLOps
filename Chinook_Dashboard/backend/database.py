import sqlite3

def get_connection():
    """데이터베이스에 연결을 설정합니다."""
    try:
        conn = sqlite3.connect('./backend/Chinook_Sqlite.sqlite')
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def get_album_count():
    """각 아티스트의 앨범 수를 가져옵니다."""
    conn = get_connection()
    if conn is None:
        return []
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT Artist.Name AS ArtistName, COUNT(Album.AlbumId) AS AlbumCount
            FROM Album
            JOIN Artist ON Album.ArtistId = Artist.ArtistId
            GROUP BY Artist.ArtistId
            ORDER BY AlbumCount DESC;
        """)
        data = cursor.fetchall()
        return data
    except sqlite3.Error as e:
        print(f"Error executing query: {e}")
        return []
    finally:
        conn.close()

def get_track_count_in_album():
    """각 앨범의 트랙 수를 가져옵니다."""
    conn = get_connection()
    if conn is None:
        return []
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT Album.Title AS AlbumTitle, COUNT(Track.TrackId) AS TrackCount
            FROM Track
            JOIN Album ON Track.AlbumId = Album.AlbumId
            GROUP BY Album.AlbumId
            ORDER BY TrackCount DESC;
        """)
        data = cursor.fetchall()
        return data
    except sqlite3.Error as e:
        print(f"Error executing query: {e}")
        return []
    finally:
        conn.close()

def get_track_count_in_playlist():
    """각 플레이리스트의 트랙 수를 가져옵니다."""
    conn = get_connection()
    if conn is None:
        return []
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT Playlist.Name AS PlaylistName, COUNT(PlaylistTrack.TrackId) AS TrackCount
            FROM Playlist
            JOIN PlaylistTrack ON Playlist.PlaylistId = PlaylistTrack.PlaylistId
            GROUP BY Playlist.PlaylistId
            ORDER BY TrackCount DESC;
        """)
        data = cursor.fetchall()
        return data
    except sqlite3.Error as e:
        print(f"Error executing query: {e}")
        return []
    finally:
        conn.close()

def get_top_artists_data(limit: int):
    """트랙 수 기준 상위 아티스트 데이터를 가져옵니다."""
    conn = get_connection()
    if conn is None:
        return []
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT Artist.Name AS ArtistName, COUNT(Track.TrackId) AS TrackCount
            FROM Artist
            JOIN Album ON Artist.ArtistId = Album.ArtistId
            JOIN Track ON Album.AlbumId = Track.AlbumId
            GROUP BY Artist.ArtistId
            ORDER BY TrackCount DESC
            LIMIT ?;
        """, (limit,))
        data = cursor.fetchall()
        return data
    except sqlite3.Error as e:
        print(f"Error executing query: {e}")
        return []
    finally:
        conn.close()
