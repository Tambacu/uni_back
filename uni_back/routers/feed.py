from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from uni_back.database import get_session
from uni_back.models import Event, User
from uni_back.schemas import EventPublic, EventSchema, EventList
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
    event_with_username = session.scalar(select(User).where(User.id == user.id))
    if not event.image.startswith("data:image/png;base64,"):
        event.image = f"data:image/png;base64,{event.image}"

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
        "id": db_event.id,
        "title": db_event.title,
        'name': event_with_username.name
    }

    return response


@router.get('/home', response_model=EventList)
def get_events_home(session: Session, skip: int = 0, limit: int = 15):
    events_array = []
    events = session.scalars(select(Event).offset(skip).limit(limit)).all()
    for event in events:

        events_array.append(event)

    return events_array
