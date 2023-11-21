from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import List

from .db import db

class Room(db.Model):
    __tablename__ = "room"
    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str] = mapped_column(unique=True)
    date_created: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow)
    # checklists: Mapped[List["CheckList"]] = relationship("CheckList", back_populates="room", cascade="all, delete", passive_deletes=True,)
    checklists: Mapped[List["CheckList"]] = relationship(cascade="all, delete",)
    
    def __init__(self, uuid=None, name=None, date_created=None):
        self.uuid = uuid
        self.name = name
        self.date_created = date_created

    def __repr__(self):
        return f'<Room {self.uuid!r}>'
    
class CheckList(db.Model):
    __tablename__ = 'check_list'
    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(nullable=False)
    room_id: Mapped[str] = mapped_column(db.ForeignKey('room.uuid', ondelete='CASCADE'), nullable=False)
    # room: Mapped[List["Room"]] = relationship("Room", back_populates="checklists")

    def __init__(self, room_id=None, content=None):
        self.room_id = room_id
        self.content = content

    def __repr__(self):
        return f'<CheckList {self.room_id!r}>'
    
    def __len__(self):
        return len(self.room_id)