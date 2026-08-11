from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from supabase_client import supabase
from fastapi import Header

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

@router.post("/auth/login")
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

@router.get("/public/info")
def get_public_info():
    return {"message": "This is a public endpoint accessible without authentication."}

@router.get("/protected/info")
def get_protected_info(authorization: str = Header(None)):
    if not authorization or not authorization.lower().startswith("Bearer ") or len(authorization.split(" ")) < 2:
        raise HTTPException(status_code=401, detail={"error": "Access token is missing or invalid"})
    token = authorization.split(" ")[1]
    return {"token_received": bool(token)}
