from fastapi import APIRouter, HTTPException, status
from app.schemas.notes import Note

router = APIRouter()

notes = []
next_id = 1


@router.get("/notes")
def get_notes():
    return {"notes": notes}


@router.post("/notes", status_code=status.HTTP_201_CREATED)
def post_notes(note: Note):
    global next_id

    new_note = {
        "id": next_id,
        "title": note.title,
        "content": note.content
    }

    next_id += 1
    notes.append(new_note)

    return {
        "message": "note posted",
        "note": new_note
    }


@router.get("/notes/{note_id}")
def get_note(note_id: int):
    for note in notes:
        if note["id"] == note_id:
            return note

    raise HTTPException(status_code=404, detail="Note not found")


@router.put("/notes/{note_id}")
def update_note(note_id: int, updated_note: Note):
    for note in notes:
        if note["id"] == note_id:
            note["title"] = updated_note.title
            note["content"] = updated_note.content

            return {
                "message": "note updated",
                "note": note
            }

    raise HTTPException(status_code=404, detail="Note not found")


@router.delete("/notes/{note_id}")
def delete_note(note_id: int):
    for note in notes:
        if note["id"] == note_id:
            notes.remove(note)

            return {
                "message": "note deleted"
            }

    raise HTTPException(status_code=404, detail="Note not found")