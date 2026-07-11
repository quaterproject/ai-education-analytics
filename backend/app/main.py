from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logging import setup_logging, logger
from app.core.exceptions import EduPilotException
from app.api.v1.router import api_router
from app.ml.inference.predictor import predictor

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup ---
    setup_logging()
    logger.info(f"Initializing {settings.APP_NAME}...")
    
    # Pre-load PyTorch Model and Preprocessors
    predictor.load_model()
    
    yield
    
    # --- Shutdown ---
    logger.info(f"Shutting down {settings.APP_NAME}...")

app = FastAPI(
    title=settings.APP_NAME,
    description="Intelligent Student Success Co-Pilot API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Configuration
origins = [
    settings.FRONTEND_URL,
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom Exception Handler for EduPilotExceptions
@app.exception_handler(EduPilotException)
async def edupilot_exception_handler(request: Request, exc: EduPilotException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details
            }
        }
    )

# General Exception Handler to prevent leakage of internal stacktraces
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled server error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred on the server.",
                "details": str(exc) if settings.DEBUG else None
            }
        }
    )

# Include main router
app.include_router(api_router, prefix="/api/v1")
