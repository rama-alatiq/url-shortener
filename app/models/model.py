
from pydantic import BaseModel, HttpUrl


class shortenRequest(BaseModel):
    url:HttpUrl
    custom_alias:str|None=None


class ShortenResponse(BaseModel):
    short_url:str
    alias:str

    

    
