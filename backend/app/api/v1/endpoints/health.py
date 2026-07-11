from fastapi import APIRouter

router = APIRouter()

@router.get("")
async def get_health():
    return {
        "status": "ok",
        "service": "EduPilot AI",
        "api_version": "v1.0.0"
    }
