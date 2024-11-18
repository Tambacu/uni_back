from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select

from uni_back.database import get_session
from uni_back.models import User, Event
from uni_back.schemas import EventSchema, EventPublic
from uni_back.security import get_current_user
import base64

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

@router.get('/home')
def get_events_home(
        session: Session,
        skip: int = 0,
        limit: int = 15
):
    events = session.scalars(select(Event).offset(skip).limit(limit)).all()
    events_with_decoded_images = []
    for event in events:
        decoded_image = None
        if event.image:
            try:
                decoded_image = base64.b64decode(event.image)
            except Exception as e:
                print(f"Erro ao decodificar imagem base64 para o evento {event.id}: {e}")
                print(decoded_image)
        events_with_decoded_images.append({
            "id": event.id,
            "title": event.title,
            "description": event.description,
            "image": decoded_image,
            "likes": event.likes,
        })

    return {"events": events_with_decoded_images}
