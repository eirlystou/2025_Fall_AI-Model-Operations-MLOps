from fastapi import FastAPI
from backend.database import get_top_artists_data, get_album_count, get_track_count_in_album, get_track_count_in_playlist
from backend.schemas import TopArtist
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/top_artists/{limit}", response_model=list[TopArtist])
def get_top_artists(limit: int):
    data = get_top_artists_data(limit)
    return JSONResponse(content=[{"ArtistName": row[0], "TrackCount": row[1]} for row in data])

@app.get("/album_count/{limit}")
def album_count(limit: int):
    data = get_album_count()
    return {"data": data}

@app.get("/track_count_in_album/{limit}")
def track_count_in_album(limit: int):
    data = get_track_count_in_album()
    return {"data": data}

@app.get("/track_count_in_playlist/{limit}")
def track_count_in_playlist(limit: int):
    data = get_track_count_in_playlist()
    return {"data": data}
