from db import engine, init_db
from models import Album, Band
from sqlmodel import Session

BANDS: list[dict] = [
    {"name": "The Kinks", "genre": "Rock"},
    {"name": "Aphex Twin", "genre": "Electronic"},
    {
        "name": "Slowdive",
        "genre": "Shoegaze",
        "albums": [
            {"title": "Master of Reality", "release_date": "1971-07-21"},
            {"title": "Master of Reality2", "release_date": "1980-07-21"},
        ],
    },
    {"name": "Wu-Tang Clan", "genre": "Hip-Hop"},
    {"name": "John Doe", "genre": "Rock"},
]


def main():
    init_db()
    session = Session(engine)

    for band_data in BANDS:
        band = Band.model_validate(band_data)
        session.add(band)
        if band_data.get("albums"):
            for album_data in band_data["albums"]:
                album = Album.model_validate(album_data)
                album.band = band
                session.add(album)

    session.commit()
    session.close()


if __name__ == "__main__":
    main()
