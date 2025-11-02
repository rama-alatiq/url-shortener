
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routers.url_shortner import router as url_shortner
# from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app:FastAPI):   
    yield

app=FastAPI(lifespan=lifespan)
app.include_router(url_shortner)

# origins = [
#     "http://127.0.0.1:8001",
#     "http://localhost:8001",
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,           
#     allow_credentials=True,           
#     allow_methods=["*"],          
#     allow_headers=["*"],          
# )
