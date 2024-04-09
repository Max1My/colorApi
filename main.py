import uvicorn
from fastapi import FastAPI
from fastapi_pagination import add_pagination
from starlette.middleware.cors import CORSMiddleware

from src.api import api_router

origins = [
    '*'
]


class ColorAPI(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


def run_server():
    uvicorn.run("main:get_application", reload=True, host='0.0.0.0', port=8000)


def get_application():
    app = ColorAPI()
    app.include_router(api_router)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    add_pagination(app)
    return app


if __name__ == "__main__":
    run_server()
