from app.database import get_db
from fastapi import APIRouter, HTTPException, status, Depends, Query
from app.schemas.notes import MessageResponse, NoteCreate, NoteResponse, PaginatedNotes
from app.services.notes import create_note, delete_note, get_all_notes, get_note_by_id, update_note
from sqlalchemy.orm import  Session
from app.dependencies import get_current_user
from app.exceptions import NoteNotFoundException
from app.models import User
from typing import Literal
router = APIRouter()



@router.get("/notes", response_model=PaginatedNotes)
def get_notes(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    sort_by: Literal["created_at", "updated_at", "title"] = Query("created_at"),
    order: Literal["asc", "desc"] = Query("desc"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    notes, total = get_all_notes(db, current_user.id, skip, limit, sort_by, order)
    return {"total": total, "skip": skip, "limit": limit, "items": notes}

    


@router.post("/notes", status_code=status.HTTP_201_CREATED, response_model=NoteResponse)
def post_notes(note: NoteCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_note = create_note(db, note, current_user.id)
    return db_note


@router.get("/notes/{note_id}", response_model=NoteResponse)
def get_note(note_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        note = get_note_by_id(db, note_id, current_user.id)
        return note
    except NoteNotFoundException:
        raise HTTPException(status_code=404, detail="Note not found")


@router.put("/notes/{note_id}", response_model=NoteResponse)
def put_note(note_id: int, updated_note: NoteCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        note = update_note(db, note_id, updated_note, current_user.id)
        return note
    except NoteNotFoundException:
        raise HTTPException(status_code=404, detail="Note not found")

@router.delete("/notes/{note_id}", response_model=MessageResponse)
def delete_note_endpoint(note_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        delete_note(db, note_id, current_user.id)
        return {"message": "Note deleted successfully."}
    except NoteNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")