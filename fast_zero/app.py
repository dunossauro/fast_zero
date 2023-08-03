from fastapi import FastAPI, HTTPException

from fast_zero.schemas import Message, UserDB, UserList, UserPublic, UserSchema

app = FastAPI()


@app.get('/')
def read_root():
    return {'message': 'Olar Mundo!'}


database = []  # PROVISORIO


@app.post('/users/', response_model=UserPublic, status_code=201)
def create_user(user: UserSchema):
    user_with_id = UserDB(**user.model_dump(), id=len(database) + 1)

    database.append(user_with_id)

    return user_with_id


@app.get('/users/', response_model=UserList)
def list_users():
    return {'users': database}


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(status_code=404, detail='User not Found')

    user_with_id = UserDB(**user.model_dump(), id=user_id)
    database[user_id - 1] = user_with_id

    return user_with_id


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(status_code=404, detail='User not Found')

    del database[user_id - 1]

    return {'detail': 'User deleted'}
