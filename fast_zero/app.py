from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import Message, UserList, UserPublic, UserSchema

app = FastAPI()


@app.get('/')
def read_root():
    return {'message': 'Olar Mundo!'}


database = []  # PROVISORIO


@app.post('/users/', response_model=UserPublic, status_code=201)
def create_user(user: UserSchema, session: Session = Depends(get_session)):
    query = select(User).where(User.email == user.email)

    user_db = session.scalar(query)

    if user_db:
        raise HTTPException(
            status_code=400, detail='Username already registered'
        )

    user_db = User(
        username=user.username, password=user.password, email=user.email
    )

    session.add(user_db)
    session.commit()
    session.refresh(user_db)

    return user_db


@app.get('/users/', response_model=UserList)
def list_users(session: Session = Depends(get_session)):
    database = session.scalars(select(User)).all()
    return {'users': database}


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(
    user_id: int, user: UserSchema, session: Session = Depends(get_session)
):
    user_db = session.scalar(select(User).where(User.id == user_id))

    if not user_db:
        raise HTTPException(status_code=404, detail='User not found')

    user_db.email = user.email
    user_db.password = user.password
    user_db.username = user.username

    session.commit()
    session.refresh(user_db)

    return user_db


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user_db = session.scalar(select(User).where(User.id == user_id))

    if not user_db:
        raise HTTPException(status_code=404, detail='User not Found')

    session.delete(user_db)
    session.commit()

    return {'detail': 'User deleted'}
