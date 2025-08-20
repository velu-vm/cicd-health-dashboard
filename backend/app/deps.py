from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from .db import get_db

async def get_current_user(session: AsyncSession = Depends(get_db)):
    """Dependency to get current authenticated user"""
    # TODO: Implement actual authentication
    # For now, return a mock user
    return {"id": 1, "username": "admin", "email": "admin@example.com"}

async def get_current_active_user(current_user = Depends(get_current_user)):
    """Dependency to get current active user"""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return current_user

def get_pagination_params(
    skip: int = 0,
    limit: int = 100
):
    """Dependency to get pagination parameters"""
    if skip < 0:
        skip = 0
    if limit < 1 or limit > 1000:
        limit = 100
    return {"skip": skip, "limit": limit}
