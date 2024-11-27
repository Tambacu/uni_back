from http import HTTPStatus
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from uni_back.database import get_session
from uni_back.models import Event, User
from uni_back.schemas import EventHome, EventPublic, EventSchema, Message
from uni_back.security import get_current_user

router = APIRouter(prefix='/event', tags=['events'])
Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', response_model=EventPublic)
def create_event(
    event: EventSchema,
    session: Session,
    user: CurrentUser,
):
    event_with_username = session.scalar(
        select(User).where(User.id == user.id)
    )
    if not event.image.startswith('data:image/png;base64,'):
        event.image = f'data:image/png;base64,{event.image}'

    db_event = Event(
        title=event.title,
        image=event.image,
        description=event.description,
        location=event.location,
        date=event.date,
        user_id=user.id,
    )

    session.add(db_event)
    session.commit()
    session.refresh(db_event)

    response = {
        'id': db_event.id,
        'title': db_event.title,
        'name': event_with_username.name,
    }

    return response


@router.get('/home', response_model=List[EventHome])
def get_events_home(
    session: Session,
):
    events = session.scalars(select(Event))
    # for event in events:
    #     events_array.append(event)

    return events


@router.delete('/home/{event_id}', response_model=Message)
def delete_event(
    event_id: int,
    session: Session,
):
    db_event = session.scalar(select(Event).where(Event.id == event_id))

    if not db_event:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )
    session.delete(db_event)
    session.commit()

    return {'message': 'Event deleted'}
