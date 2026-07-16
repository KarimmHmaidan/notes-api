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

def get_all_notes(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 10,
    sort_by: str = "created_at",
    order: str = "desc",
):
    sortable_fields = {
        "created_at": models.Note.created_at,
        "updated_at": models.Note.updated_at,
        "title": models.Note.title,
    }
    sort_column = sortable_fields.get(sort_by, models.Note.created_at)

    if order == "asc":
        sort_column = sort_column.asc()
    else:
        sort_column = sort_column.desc()

    query = db.query(models.Note).filter(models.Note.owner_id == user_id)
    total = query.count()
    notes = query.order_by(sort_column).offset(skip).limit(limit).all()
    return notes, total

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
