from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db, get_current_user_email
from models import ChatMessage
from schemas import ChatCreate, ChatOut

from typing import List
from datetime import datetime

router = APIRouter()


@router.post("/groups/{group_id}/chat", response_model=ChatOut)
def send_message(group_id: int, chat: ChatCreate, db: Session = Depends(get_db), user_email: str = Depends(get_current_user_email)):
    new_message = ChatMessage(
        group_id=group_id,
        sender_email=user_email,
        content=chat.message,
        timestamp=datetime.utcnow()
    )
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return ChatOut(sender=new_message.sender_email, content=new_message.content, timestamp=new_message.timestamp)


@router.get("/groups/{group_id}/chat", response_model=List[ChatOut])
def get_chat_messages(group_id: int, db: Session = Depends(get_db)):
    messages = db.query(ChatMessage).filter(ChatMessage.group_id == group_id).order_by(ChatMessage.timestamp).all()
    return [ChatOut(sender=m.sender_email, content=m.content, timestamp=m.timestamp) for m in messages]
