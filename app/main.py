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

@app.put("/notes/{note_id}")
def update_note(note_id: int, updated_note: Note):
    for note in notes:
        if note["id"] == note_id:
            note["title"] = updated_note.title
            note["content"] = updated_note.content
            return {"message": "note updated",
                    "note": note}
    raise HTTPException(status_code = 404)

@app.delete("/notes/{note_id}")
def delete_note(note_id: int):
    for note in notes:
        if note["id"] == note_id:
            notes.remove(note)
            return {"message": "note deleted"}
    raise HTTPException(status_code = 404, detail="Note not found")



