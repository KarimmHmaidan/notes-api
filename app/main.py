from fastapi import FastAPI
from app.routers.notes import router as notes_router
from app.database import engine
from app.models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Welcome to Notes API"}


app.include_router(notes_router)



