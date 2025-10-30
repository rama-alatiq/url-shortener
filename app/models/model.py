
from pydantic import BaseModel, HttpUrl
from sqlmodel import Field, SQLModel


class URL(SQLModel, table=True):
    alias: str = Field(primary_key=True)
    url: str = Field(default=None, nullable=False)


class ShortenRequest(BaseModel):
    url: HttpUrl
    custom_alias: str | None = None


class ShortenResponse(BaseModel):
    short_url: str
    alias: str

    
