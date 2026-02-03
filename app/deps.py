from fastapi import Header, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.security import decode_token
from app.models.todo import Todo
from app.models.todo_share import TodoShare
from sqlalchemy.orm import Session
from fastapi import HTTPException

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    payload = decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    if payload.get("type") != "access":
        raise HTTPException(
            status_code=401,
            detail="Invalid access token"
        )

    return payload


def require_admin(payload: dict = Depends(get_current_user)):
    if payload.get("role") != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    return payload

def get_task_permission(
    task_id: int,
    user_id: int,
    db: Session
):
    task = db.query(Todo).filter(Todo.id == task_id).first()
    if not task:
        raise HTTPException(404, "Task not found")

    if task.user_id == user_id:
        return "owner"

    share = db.query(TodoShare).filter(
        TodoShare.todo_id == task_id,
        TodoShare.user_id == user_id
    ).first()

    if not share:
        raise HTTPException(403, "No access to this task")

    return share.permission