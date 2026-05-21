from sqlalchemy import Column,Integer,Text,DateTime,func
from .base import Base

class ChatHistory(Base):
    __tablename__="chat_history"
    id=Column(Integer,primary_key=True,index=True)
    question=Column(Text,nullable=False)
    answer=Column(Text,nullable=False)
    created_at=Column(DateTime,server_default=func.now())