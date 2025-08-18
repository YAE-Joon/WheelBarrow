from fastapi import FastAPI
from app.core.config import settings
from app.controllers import auth_controller
from app.controllers import category_controller
from app.controllers import work_controller
from app.core.middlewares import cors_middleware
from contextlib import asynccontextmanager
import logging

#로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title =settings.app_name,
    version = "1.0.0",
    debug=settings.debug) # api for json

app.include_router(auth_controller.router, prefix = "/api/v1")
app.include_router(category_controller.router, prefix = "/api/v1")
app.include_router(work_controller.router, prefix="/api/v1")

# add middlewares
cors_middleware.add(app)

@app.get("/")
def read_root():
    return {"message":"Welcome to FastAPI"}

# AWS 배포용 health check 추가
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "environment": settings.environment,
        "app_name": settings.app_name
    }

if __name__=="__main__":
    import uvicorn
    uvicorn.run(
        app,
        host= settings.host,
        port= settings.port,
        log_level = settings.log_level.lower()
    )