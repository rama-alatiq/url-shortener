import secrets
import string
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
from app.models.model import ShortenRequest, ShortenResponse, URL
from app.deps.deps import SessionDep



router=APIRouter(tags=["shortner"])


alphabet=string.ascii_letters+string.digits
def generate_alias(length:int=6)->str:
    return "".join(secrets.choice(alphabet) for _ in range(length))



@router.post("/shorten", response_model=ShortenResponse)
async def url_shortner(payload: ShortenRequest, request: Request, session: SessionDep):

    alias = payload.custom_alias.strip() if payload.custom_alias else None
    
    if alias:
        if session.get(URL, alias):
            raise HTTPException(status_code=400, detail=f"Custom alias '{alias}' is already in use.")
            
    else: 
        for _ in range(10): 
            candidate = generate_alias() 
            if not session.get(URL, candidate):
                alias = candidate 
                break
        else:
            raise HTTPException(status_code=500, detail="Server failed to generate a unique alias.")
            
    
    db_url = URL(alias=alias, url=str(payload.url))
    session.add(db_url)
    session.commit()
    session.refresh(db_url)

    base = str(request.base_url).rstrip("/")
    return ShortenResponse(short_url=f"{base}/{alias}", alias=alias)    



@router.get("/{short_id}")
async def redirect_to_long_url(short_id: str, session: SessionDep):
    db_url = session.get(URL, short_id)

    if db_url is None:
        raise HTTPException(status_code=404, detail="Short URL not found")

  #temp redirect
    return RedirectResponse(url=db_url.url, status_code=307)