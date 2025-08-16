from fastapi import FastAPI
from app.core.database import engine, Base
from app.controllers import auth_controller
from app.controllers import category_controller
from app.controllers import work_controller
from app.core.middlewares import cors_middleware
from contextlib import asynccontextmanager
import logging

#로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title ="FASTAPI MVC EXAMPLE",version = "1.0.0") # api for json

app.include_router(auth_controller.router, prefix = "/api/v1")
app.include_router(category_controller.router, prefix = "/api/v1")
app.include_router(work_controller.router, prefix="/api/v1")

# add middlewares
cors_middleware.add(app)

@app.get("/")
def read_root():
    return {"message":"Welcome to FastAPI"}

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app, host= "0.0.0.0", port=8000,log_level = "debug")