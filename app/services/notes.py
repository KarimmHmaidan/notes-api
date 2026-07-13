from sqlalchemy.orm import Session
from app import models
from app.schemas.notes import NoteCreate
from app.exceptions import NoteNotFoundException

def create_note(db: Session, note: NoteCreate, user_id: int):
    db_note = models.Note(title=note.title, content=note.content, owner_id=user_id)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

def get_all_notes(db: Session, user_id: int):
    notes= db.query(models.Note).filter(models.Note.owner_id == user_id).all()
    if not notes:
        return []
    return notes
        

def get_note_by_id(db: Session, note_id: int, user_id: int):
    note = db.query(models.Note).filter(models.Note.id == note_id, models.Note.owner_id == user_id).first()
    if not note:
        raise NoteNotFoundException("Note not found.")
    return note

def update_note(db: Session, note_id: int, updated_note: NoteCreate, user_id: int):
    note = db.query(models.Note).filter(models.Note.id == note_id, models.Note.owner_id == user_id).first()
    if not note:
        raise NoteNotFoundException("Note not found.")
    note.title = updated_note.title
    note.content = updated_note.content
    db.commit()
    db.refresh(note)
    return note



def delete_note(db: Session, note_id: int, user_id: int):
    note = db.query(models.Note).filter(models.Note.id == note_id, models.Note.owner_id == user_id).first()
    if not note:
        raise NoteNotFoundException("Note not found.")
    db.delete(note)
    db.commit()
    return note
