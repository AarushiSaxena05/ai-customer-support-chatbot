from app.db.database import SessionLocal
from sqlalchemy import Column, Integer, String
from app.db.database import Base

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    message = Column(String)
    response = Column(String)

def save_message(user_id, message, response):
    db = SessionLocal()
    convo = Conversation(user_id=user_id, message=message, response=response)
    db.add(convo)
    db.commit()
    db.close()

def get_history(user_id, limit=5):
    db = SessionLocal()
    data = db.query(Conversation).filter_by(user_id=user_id)\
        .order_by(Conversation.id.desc()).limit(limit).all()
    db.close()
    return [(d.message, d.response) for d in data]