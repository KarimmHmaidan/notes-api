from app.database import get_db
from app.services import notes
from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.notes import MessageResponse, Note, NoteResponse
from app.services.notes import create_note, delete_note, get_all_notes, get_note_by_id, update_note
from sqlalchemy.orm import Session

router = APIRouter()



@router.get("/notes", response_model=list[NoteResponse])
def get_notes(db: Session = Depends(get_db)):
    notes = get_all_notes(db)
    return notes

    


@router.post("/notes", status_code=status.HTTP_201_CREATED, response_model=NoteResponse)
def post_notes(note: Note, db: Session = Depends(get_db)):
    db_note = create_note(db, note)
    return db_note


@router.get("/notes/{note_id}", response_model=NoteResponse)
def get_note(note_id: int, db: Session = Depends(get_db)):
    note = get_note_by_id(db, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.put("/notes/{note_id}", response_model=NoteResponse)
def put_note(note_id: int, updated_note: Note, db: Session = Depends(get_db)):
    note = update_note(db, note_id, updated_note)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.delete("/notes/{note_id}", response_model=MessageResponse)
def delete_note_endpoint(note_id: int, db: Session = Depends(get_db)):
    success = delete_note(db, note_id)
    if not success:
        raise HTTPException(status_code=404, detail="Note not found")
    return {
        "message": "note deleted"
    }