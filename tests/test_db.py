from dataclasses import asdict

from sqlalchemy import select

from fastapi_zero.database import get_session
from fastapi_zero.models import User


def test_get_session():
    session_generator = get_session()
    session = next(session_generator)

    assert session is not None

    session.close()


def test_create_user(session, mock_db_time):

    with mock_db_time(model=User) as time:
        new_user = User(
            username='test',
            email='test@test.com',
            password='secret',
        )

        session.add(new_user)
        session.commit()

        user = session.scalar(select(User).where(User.username == 'test'))

    assert asdict(user) == {
        'id': 1,
        'username': 'test',
        'email': 'test@test.com',
        'password': 'secret',
        'created_at': time,
        'updated_at': time,
    }
