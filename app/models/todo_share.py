from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from app.database.base import Base

class TodoShare(Base):
    __tablename__ = "todo_shares"

    id = Column(Integer, primary_key=True)
    todo_id = Column(Integer, ForeignKey("todos.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    permission = Column(String, nullable=False)  # viewer | editor

    __table_args__ = (
        UniqueConstraint("todo_id", "user_id"),
    )
