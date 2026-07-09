from fastapi import FastAPI
from app.routers.notes import router as notes_router

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Welcome to Notes API"}


app.include_router(notes_router)



