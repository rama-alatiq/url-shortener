import secrets
import string
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
# from app.deps.deps import SessionDep
from app.models.model import shortenRequest,ShortenResponse


router=APIRouter(tags=["shortner"])

store:dict[str,str]={}
alphabet=string.ascii_letters+string.digits
def generate_alias(length:int=6)->str:
    return "".join(secrets.choice(alphabet) for _ in range(length))



@router.post("/shorten")
async def url_shortner(payload: shortenRequest, request: Request):

    alias = payload.custom_alias.strip() if payload.custom_alias else None
    
    if alias:
        if alias in store: 
            raise HTTPException(status_code=400, detail=f"Custom alias '{alias}' is already in use.")
            
    else: 
        for _ in range(10): 
            candidate = generate_alias() 
            if candidate not in store:
                alias = candidate 
                break
        else:
            raise HTTPException(status_code=500, detail="Server failed to generate a unique alias.")
            
    
    store[alias] = str(payload.url) 
    base = str(request.base_url).rstrip("/")
    return ShortenResponse(short_url=f"{base}/{alias}", alias=alias)    



@router.get("/{short_id}")
async def redirect_to_long_url(short_id: str):
    long_url = store.get(short_id) 

    if long_url is None:
        raise HTTPException(status_code=404, detail="Short URL not found")

  #temp redirect
    return RedirectResponse(url=long_url, status_code=307)