# from sqlalchemy.orm import Session
# from app.models.todo import Todo

# def create_task(db: Session, data, user_id: int):
#     task = Todo(**data.dict(), user_id=user_id)
#     db.add(task)
#     db.commit()
#     db.refresh(task)
#     return task

# def get_tasks(db: Session, user_id: int):
#     return db.query(Todo).filter(Todo.user_id == user_id).all()

# def update_task(db: Session, task_id: int, data, user_id: int):
#     task = db.query(Todo).filter(
#         Todo.id == task_id,
#         Todo.user_id == user_id
#     ).first()
#     if not task:
#         return None

#     for k, v in data.dict().items():
#         setattr(task, k, v)

#     db.commit()
#     return task

# def delete_task(db: Session, task_id: int, user_id: int):
#     task = db.query(Todo).filter(
#         Todo.id == task_id,
#         Todo.user_id == user_id
#     ).first()
#     if not task:
#         return None
#     db.delete(task)
#     db.commit()
#     return True
