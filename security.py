from fastapi import Depends, HTTPException
from supabase_client import supabase
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

bearer_scheme = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials
    try:
        response = supabase.auth.get_user(token)
        user = response.user
        if user is None:
            raise ValueError("No user returned")
        return user
    except Exception:
        raise HTTPException(status_code=401, detail={"error": "Invalid or expired token"})

    

