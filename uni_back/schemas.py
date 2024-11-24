from pydantic import BaseModel, EmailStr


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    name: str
    email: EmailStr
    password: str
    cpf: str
    phone_number: str


class UserPublic(BaseModel):
    name: str
    email: EmailStr
    id: int


class UserDB(UserSchema):
    id: int


class UserList(BaseModel):
    users: list[UserPublic]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class EventSchema(BaseModel):
    title: str
    image: str
    description: str


class EventPublic(BaseModel):
    title: str
    id: int


class EventHome(BaseModel):
    id: int
    title: str
    description: str
    image: str
    likes: int


class EventList(BaseModel):
    events: list[EventHome]
