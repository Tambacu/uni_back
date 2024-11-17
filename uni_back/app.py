from http import HTTPStatus

from fastapi import FastAPI

from uni_back.routers import auth, feed, users
from uni_back.schemas import Message

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(feed.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def root():
    return {'message': 'Hello World'}
