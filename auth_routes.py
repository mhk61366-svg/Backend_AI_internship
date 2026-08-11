from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from supabase_client import supabase
from security import get_current_user

router = APIRouter()

class AuthCredentials(BaseModel):
    email: str
    password: str

@router.post("/auth/signup",status_code=201)
def sign_up(credentials: AuthCredentials):
    if not credentials.email or not credentials.password:
        raise HTTPException(status_code=400, detail={"error": "Email and password are required"})
    try:
        response = supabase.auth.sign_up({
            "email": credentials.email,
            "password": credentials.password
        })
        return {"data": response.user}
    except Exception as e:
        raise HTTPException(status_code=400, detail={"error": str(e)})

@router.post("/auth/login", status_code=200)
def login(credentials: AuthCredentials):
    if not credentials.email or not credentials.password:
        raise HTTPException(status_code=400, detail={"error": "Email and password are required"})
    try:
        response = supabase.auth.sign_in_with_password({
            "email": credentials.email,
            "password": credentials.password
        })
    except Exception:
        raise HTTPException(status_code=401, detail={"error": "Invalid login credentials"})

    if response.session is None:
        raise HTTPException(status_code=401, detail={"error": "Invalid login credentials"})

    return {
        "access_token": response.session.access_token,
        "refresh_token": response.session.refresh_token
    }

@router.post("/auth/logout", status_code=204)
def logout(user=Depends(get_current_user)):
    supabase.auth.sign_out()
    return

@router.get("/public/info",status_code=200)
def get_public_info():
    return {"message": "This is a public endpoint accessible without authentication."}

@router.get("/protected/info",status_code=200)
def get_protected_info(user: dict = Depends(get_current_user)):
    return {"user id": user.id, "user email": user.email, "created_at": user.created_at}

@router.get("/protected/dashboard",status_code=200)
def get_dashboard(user: dict = Depends(get_current_user)):
    return {"message": f"Welcome to your dashboard, {user.email}!"}