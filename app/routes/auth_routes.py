from fastapi import APIRouter, Depends, HTTPException, Cookie
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.controllers.auth_controller import register_user, authenticate_user
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.models.user import User
from app.deps import get_current_user
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse

router = APIRouter(tags=["Auth"])


@router.get("/", include_in_schema=False)
def index_page():
    return FileResponse("static/index.html")


@router.get("/login", include_in_schema=False)
def login_page():
    return FileResponse("static/login.html")


@router.get("/register", include_in_schema=False)
def register_page():
    return FileResponse("static/register.html")

@router.get("/admin", include_in_schema=False)
def admin_page():
    return FileResponse("static/admin.html")


@router.post("/register")
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db)
):
    try:
        user = register_user(db, data.name, data.email, data.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not user:
        raise HTTPException(status_code=400, detail="Registration failed")

    return {"success": True}


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    """
    Authenticate user and return access & refresh tokens.
    """
    user = authenticate_user(db, data.email, data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(user.id,user.role)
    refresh_token = create_refresh_token(user.id,user.role)

    response = JSONResponse(
        {
            "access_token": access_token,
            "token_type": "bearer",
        }
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
    )

    return response


@router.post("/refresh")
def refresh(refresh_token: str = Cookie(None)):
    """
    Generate a new access token using a valid refresh token.
    """
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")

    payload = decode_token(refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    user_id = int(payload["sub"])
    role = payload["role"]

    new_access = create_access_token(user_id, role)
    new_refresh = create_refresh_token(user_id, role)

    response = JSONResponse(
        {
            "access_token": new_access,
            "token_type": "bearer",
        }
    )

    response.set_cookie(
        key="refresh_token",
        value=new_refresh,
        httponly=True,
        secure=True,
        samesite="strict",
    )

    return response


@router.post("/logout")
def logout():
    res = JSONResponse({"success": True})
    res.delete_cookie("refresh_token")
    return res


@router.get("/me")
def me(
    payload: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Return current authenticated user's profile information.
    """
    user_id = int(payload["sub"])
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404)
    return {"name": user.name, "email": user.email, "role": user.role}
