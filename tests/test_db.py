from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from uni_back.models import User, table_registry


def test_create_user():
    engine = create_engine('sqlite:///:memory:')
    table_registry.metadata.create_all(engine)
    with Session(engine) as session:
        user = User(
            name='tambas', email='tamba123@gmail.com', password='tambabao'
        )
        session.add(user)
        session.commit()
        result = session.scalar(
            select(User).where(User.email == 'tamba123@gmail.com')
        )
    assert result.name == 'tambas'
    assert result.email == 'tamba123@gmail.com'
    assert result.password == 'tambabao'
    assert result.id == 1
