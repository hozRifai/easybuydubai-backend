from fastapi import APIRouter
from app.models import HealthCheck
from app.config import settings

router = APIRouter(
    prefix="/api",
    tags=["health"],
)

@router.get("/health", response_model=HealthCheck)
async def health_check():
    """
    Health check endpoint
    """
    return HealthCheck(
        status="healthy",
        environment=settings.environment
    )

@router.get("/")
async def root():
    """
    Root endpoint
    """
    return {
        "message": "EasyBuy Dubai Property Assistant API",
        "version": "1.0.0",
        "status": "running"
    }