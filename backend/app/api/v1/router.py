from fastapi import APIRouter
from app.api.v1.endpoints import (
    health,
    students,
    predictions,
    documents,
    recommendations,
    reviews,
    analytics,
    reports
)

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(students.router, prefix="/students", tags=["students"])
api_router.include_router(documents.router, tags=["documents"])
api_router.include_router(predictions.router, tags=["predictions"])
api_router.include_router(recommendations.router, tags=["recommendations"])
api_router.include_router(reviews.router, tags=["reviews"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
api_router.include_router(reports.router, tags=["reports"])
