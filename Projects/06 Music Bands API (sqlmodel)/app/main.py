from contextlib import asynccontextmanager
from typing import Annotated, Sequence

from db import get_session, init_db
from fastapi import Depends, FastAPI, HTTPException, Path, Query
from fastapi.responses import HTMLResponse
from models import (
    Album,
    Band,
    BandCreate,
    BandPublic,
    BandPublicWithAlbums,
    GenreURLChoices,
)
from sqlmodel import Session, select


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def index() -> HTMLResponse:
    content = """
    <h1>Welcome to my API</h1>
    <p>Please check the <a href="http://127.0.0.1:8000/docs">documentation</a> page.</p>
    """
    return HTMLResponse(content)


@app.get("/bands", response_model=list[BandPublic])
def read_bands(
    genre: GenreURLChoices | None = None,
    q: Annotated[str | None, Query(max_length=20)] = None,
    session: Session = Depends(get_session),
) -> Sequence[Band]:
    band_list = session.exec(select(Band)).all()
    if genre:
        band_list = [
            band for band in band_list if band.genre.value.lower() == genre.value
        ]
    if q:
        band_list = [band for band in band_list if q.lower() in band.name.lower()]

    return band_list


@app.get("/bands/{band_id}", response_model=BandPublicWithAlbums)
def read_band(
    band_id: Annotated[int, Path(gt=0)],
    session: Session = Depends(get_session),
) -> Band:
    band = session.get(Band, band_id)
    if not band:
        raise HTTPException(status_code=404, detail="Band not found")
    return band


@app.get("/bands/genre/{genre}", response_model=list[BandPublic])
def read_bands_by_genre(
    genre: GenreURLChoices,
    session: Session = Depends(get_session),
) -> Sequence[Band]:
    return session.exec(select(Band).where(Band.genre == genre)).all()


@app.post("/bands", response_model=BandPublic)
def create_band(
    band_data: BandCreate,
    session: Session = Depends(get_session),
) -> Band:
    band = Band.model_validate(band_data.model_dump(exclude={"albums"}))
    session.add(band)
    if band_data.albums:
        for album in band_data.albums:
            album_obj = Album.model_validate(album)
            album_obj.band = band
            session.add(album_obj)
    session.commit()
    session.refresh(band)
    return band
