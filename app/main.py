from fastapi import FastAPI

from core import lifespan
from controllers.api import auth_controller
from controllers.api import user_controller

from core.middlewares import cors_middleware
from exceptions import handler

# apps
api = FastAPI(lifespan=lifespan.lifespan) # api for json

# custom exception handlers
handler.add_json(api)

# add middlewares
cors_middleware.add(api)

# include api routers
api.include_router(auth_controller.router)
api.include_router(user_controller.router)