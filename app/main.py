from fastapi import FastAPI
from app.schemas import Note
from fastapi import status
from fastapi import HTTPException


app= FastAPI()
notes = []
next_id = 1

@app.get("/")
def root():
    return {"message": "Welcome to Notes API"}


@app.get("/notes")
def get_notes():
    return notes

@app.post("/notes", status_code=status.HTTP_201_CREATED)
def post_notes(note: Note):
    global next_id
    new_note = {
        "id":  next_id,
        "title": note.title,
        "content": note.content
    }
    next_id += 1
    notes.append(new_note)
    return {"message": "note posted",
            "note": new_note }

@app.get("/notes/{note_id}")
def get_note(note_id: int):
    for note in notes:
        if note["id"] == note_id :
            return note
    raise HTTPException(status_code = 404)
        