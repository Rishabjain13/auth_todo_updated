from fastapi import FastAPI
from fastapi.security import HTTPBearer
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.database import Base, engine
from app.routes.auth_routes import router as auth_router
from app.routes.todo_routes import router as todo_router
from app.routes.admin_routes import router as admin_router
from app.routes.health import router as health_router


app = FastAPI(title="Auth Todo API",
    description="Authentication-based Todo application with RBAC and sharing",
    version="1.0.0")
security = HTTPBearer()

BASE_DIR = Path(__file__).resolve().parent

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

@app.get("/", response_class=HTMLResponse)
def dashboard():
    return (BASE_DIR / "static" / "index.html").read_text(encoding="utf-8")

@app.get("/login", response_class=HTMLResponse)
def login_page():
    return (BASE_DIR / "static" / "login.html").read_text(encoding="utf-8")

@app.get("/register", response_class=HTMLResponse)
def register_page():
    return (BASE_DIR / "static" / "register.html").read_text(encoding="utf-8")

app.include_router(auth_router)
app.include_router(todo_router)
app.include_router(admin_router)
app.include_router(health_router)



# from app.database import SessionLocal
# from app.models.user import User
# db = SessionLocal()
# admin = db.query(User).filter(User.email == "admin@email.com").first()
# admin.role = "admin"
# db.commit()

