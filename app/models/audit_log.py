from sqlalchemy import Column, Integer, String
from app.database.base import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True)
    action = Column(String)
    admin_email = Column(String)
