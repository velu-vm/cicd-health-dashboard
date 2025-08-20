from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from datetime import datetime

from .db import get_db
from .models import Alert
from .schemas import AlertCreate, AlertUpdate, Alert as AlertSchema
from .deps import get_current_active_user

router = APIRouter(tags=["alerts"])

@router.get("/alerts", response_model=List[AlertSchema])
async def get_alerts(
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Get all alerts with pagination"""
    query = select(Alert).offset(skip).limit(limit)
    result = await session.execute(query)
    alerts = result.scalars().all()
    return alerts

@router.get("/alerts/{alert_id}", response_model=AlertSchema)
async def get_alert(
    alert_id: int,
    session: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Get a specific alert by ID"""
    query = select(Alert).where(Alert.id == alert_id)
    result = await session.execute(query)
    alert = result.scalar_one_or_none()
    
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found"
        )
    return alert

@router.post("/alerts", response_model=AlertSchema, status_code=status.HTTP_201_CREATED)
async def create_alert(
    alert: AlertCreate,
    session: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Create a new alert"""
    db_alert = Alert(**alert.dict())
    session.add(db_alert)
    await session.commit()
    await session.refresh(db_alert)
    return db_alert

@router.put("/alerts/{alert_id}", response_model=AlertSchema)
async def update_alert(
    alert_id: int,
    alert_update: AlertUpdate,
    session: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Update an existing alert"""
    query = select(Alert).where(Alert.id == alert_id)
    result = await session.execute(query)
    db_alert = result.scalar_one_or_none()
    
    if not db_alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found"
        )
    
    update_data = alert_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_alert, field, value)
    
    await session.commit()
    await session.refresh(db_alert)
    return db_alert

@router.delete("/alerts/{alert_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_alert(
    alert_id: int,
    session: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Delete an alert"""
    query = select(Alert).where(Alert.id == alert_id)
    result = await session.execute(query)
    alert = result.scalar_one_or_none()
    
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found"
        )
    
    await session.delete(alert)
    await session.commit()
    return None
