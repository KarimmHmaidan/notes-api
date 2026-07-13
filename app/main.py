from fastapi import FastAPI
from app.routers.notes import router as notes_router
from app.database import engine
from app.models import Base
from app.routers.auth import router as auth_router


app = FastAPI()


@app.get("/")
def root():
    return {"message": "Welcome to Notes API"}


app.include_router(notes_router)
app.include_router(auth_router)



