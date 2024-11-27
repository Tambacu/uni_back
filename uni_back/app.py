from http import HTTPStatus

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from uni_back.routers import auth, feed, users
from uni_back.schemas import Message

app = FastAPI()
origins = [
    'http://localhost:8081',
    'http://192.168.18.13:8081',
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(feed.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def root():
    return {'message': 'Hello World'}

