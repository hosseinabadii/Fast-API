from contextlib import asynccontextmanager
from typing import Annotated

from db import get_session, init_db
from fastapi import Depends, FastAPI, HTTPException, Path, Query
from models import Album, Band, BandCreate, GenreURLChoices
from sqlmodel import Session, select


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root() -> str:
    return "Welcome to the Bands API!"


@app.get("/bands")
def read_bands(
    genre: GenreURLChoices | None = None,
    q: Annotated[str | None, Query(max_length=20)] = None,
    session: Session = Depends(get_session),
) -> list[Band]:
    band_list = session.exec(select(Band)).all()
    if genre:
        band_list = [
            band for band in band_list if band.genre.value.lower() == genre.value
        ]
    if q:
        band_list = [band for band in band_list if q.lower() in band.name.lower()]

    return band_list


@app.get("/bands/{band_id}")
def read_band(
    band_id: Annotated[int, Path(gt=0)],
    session: Session = Depends(get_session),
) -> Band:
    band = session.get(Band, band_id)
    if not band:
        raise HTTPException(status_code=404, detail="Band not found")
    return band


@app.get("/bands/genre/{genre}")
def read_bands_by_genre(
    genre: GenreURLChoices,
    session: Session = Depends(get_session),
) -> list[Band]:
    return session.exec(select(Band).where(Band.genre == genre)).all()


@app.post("/bands")
def create_band(
    band_data: BandCreate,
    session: Session = Depends(get_session),
) -> Band:
    band = Band(name=band_data.name, genre=band_data.genre)
    session.add(band)
    if band_data.albums:
        for album in band_data.albums:
            album_obj = Album(
                title=album.title, release_date=album.release_date, band=band
            )
            session.add(album_obj)
    session.commit()
    session.refresh(band)
    return band