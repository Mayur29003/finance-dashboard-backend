from fastapi import Depends, HTTPException, Header
from typing import Optional

FAKE_USERS_DB = {
    "admin1": {"role": "admin"},
    "analyst1": {"role": "analyst"},
    "viewer1": {"role": "viewer"},
}

def get_current_user(authorization: Optional[str] = Header(None)) -> dict:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token")

    username = authorization.replace("Bearer ", "", 1).strip()
    if username not in FAKE_USERS_DB:
        raise HTTPException(status_code=401, detail="Invalid user")

    return FAKE_USERS_DB[username]

def require_admin(user: dict = Depends(get_current_user)) -> dict:
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    return user

def require_analyst_or_admin(user: dict = Depends(get_current_user)) -> dict:
    if user["role"] not in ["analyst", "admin"]:
        raise HTTPException(status_code=403, detail="Analyst+ only")
    return user