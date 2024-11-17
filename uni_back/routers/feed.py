from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from uni_back.database import get_session
from uni_back.models import User, Event
from uni_back.schemas import EventSchema, EventPublic
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
    db_event = Event(
        title=event.title,
        image=event.image,
        description=event.description,
        user_id=user.id,
    )

    session.add(db_event)
    session.commit()
    session.refresh(db_event)

    return db_event
