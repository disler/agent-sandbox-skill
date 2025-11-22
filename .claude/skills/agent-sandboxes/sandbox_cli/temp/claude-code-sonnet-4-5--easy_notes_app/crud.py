from sqlalchemy.orm import Session
from datetime import datetime
from database import NoteDB
from models import NoteCreate, NoteUpdate

def get_notes(db: Session):
    return db.query(NoteDB).order_by(NoteDB.updated_at.desc()).all()

def get_note(db: Session, note_id: int):
    return db.query(NoteDB).filter(NoteDB.id == note_id).first()

def create_note(db: Session, note: NoteCreate):
    db_note = NoteDB(
        title=note.title,
        content=note.content,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

def update_note(db: Session, note_id: int, note: NoteUpdate):
    db_note = get_note(db, note_id)
    if db_note:
        if note.title is not None:
            db_note.title = note.title
        if note.content is not None:
            db_note.content = note.content
        db_note.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_note)
    return db_note

def delete_note(db: Session, note_id: int):
    db_note = get_note(db, note_id)
    if db_note:
        db.delete(db_note)
        db.commit()
        return True
    return False
