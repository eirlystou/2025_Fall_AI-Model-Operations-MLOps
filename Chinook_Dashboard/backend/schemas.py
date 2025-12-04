from pydantic import BaseModel

class TopArtist(BaseModel):
    ArtistName: str
    TrackCount: int
