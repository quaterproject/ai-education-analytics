from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.api.dependencies import get_db
from app.services.analytics_service import AnalyticsService
from app.schemas.analytics import AnalyticsOverview, RiskDistributionItem, RiskTrendItem, InterventionStatusOverview

router = APIRouter()

@router.get("/overview", response_model=AnalyticsOverview)
async def get_overview(db: AsyncSession = Depends(get_db)):
    return await AnalyticsService.get_overview(db)

@router.get("/risk-distribution", response_model=List[RiskDistributionItem])
async def get_risk_distribution(db: AsyncSession = Depends(get_db)):
    return await AnalyticsService.get_risk_distribution(db)

@router.get("/risk-trends", response_model=List[RiskTrendItem])
async def get_risk_trends(db: AsyncSession = Depends(get_db)):
    return await AnalyticsService.get_risk_trends(db)

@router.get("/intervention-status", response_model=InterventionStatusOverview)
async def get_intervention_status(db: AsyncSession = Depends(get_db)):
    return await AnalyticsService.get_intervention_status(db)
