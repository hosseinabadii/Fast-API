from datetime import date
from enum import Enum

from pydantic import field_validator
from sqlmodel import Field, Relationship, SQLModel


###-----------------------------------------------
## Genre Models
###-----------------------------------------------
class GenreURLChoices(Enum):
    Rock = "rock"
    Electronic = "electronic"
    Shoegaze = "shoegaze"
    Hip_Hop = "hip-hop"


class GenreChoices(Enum):
    Rock = "Rock"
    Electronic = "Electronic"
    Shoegaze = "Shoegaze"
    Hip_Hop = "Hip-Hop"


###-----------------------------------------------
## Album Models
###-----------------------------------------------
class AlbumBase(SQLModel):
    title: str
    release_date: date
    band_id: int | None = Field(default=None, foreign_key="band.id")


class Album(AlbumBase, table=True):
    id: int = Field(default=None, primary_key=True)
    band: "Band" = Relationship(back_populates="albums")


###-----------------------------------------------
## Band Models
###-----------------------------------------------
class BandBase(SQLModel):
    name: str
    genre: GenreChoices


class Band(BandBase, table=True):
    id: int = Field(default=None, primary_key=True)
    albums: list[Album] = Relationship(back_populates="band")


class BandCreate(BandBase):
    albums: list[AlbumBase] | None = None

    @field_validator("genre", mode="before")
    @classmethod
    def validate_genre(cls, v: str) -> str:
        return v.title()


class BandPublic(BandBase):
    id: int


class BandPublicWithAlbums(BandBase):
    id: int
    albums: list[Album] | None
