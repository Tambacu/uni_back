from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from uni_back.database import get_session
from uni_back.models import User
from uni_back.schemas import Message, UserList, UserPublic, UserSchema
from uni_back.security import get_current_user, get_password_hash

router = APIRouter(prefix='/users', tags=['users'])
T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]


@router.get('/', response_model=UserList)
def read_users(session: T_Session, skip: int = 0, limit: int = 100):
    users = session.scalars(select(User).offset(skip).limit(limit)).all()
    return {'users': users}


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: T_Session):
    db_user = session.scalar(select(User).where((User.email == user.email)))

    if db_user:
        if db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Email already exists',
            )

    hashed_password = get_password_hash(user.password)

    db_user = User(
        name=user.name,
        password=hashed_password,
        email=user.email,
        cpf=user.cpf,
        phone_number=user.phone_number,
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.put('/{user_id}', response_model=UserPublic)
def update_user(
    user_id: int,
    user: UserSchema,
    session: T_Session,
    current_user: T_CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )

    try:
        currentUser = session.scalar(select(User).where(User.id == user_id))
        if not currentUser:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail='User not found'
            )

        currentUser.name = user.name
        currentUser.password = get_password_hash(user.password)
        currentUser.email = user.email
        currentUser.cpf = user.cpf
        currentUser.phone_number = user.phone_number
        session.commit()
        session.refresh(currentUser)

        return currentUser

    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username or Email already exists',
        )


@router.delete('/{user_id}', response_model=Message)
def delete_user(user_id: int, session: T_Session, current_user: T_CurrentUser):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )

    session.delete(current_user)
    session.commit()

    return {'message': 'User deleted'}
