from fastapi.testclient import TestClient


def test_root_deve_retornar_200_e_ola_mundo(client):
    response = client.get('/')

    assert response.status_code == 200
    assert response.json() == {'message': 'Olar Mundo!'}


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'test',
            'password': 'secret',
            'email': 'test@test.com',
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        'id': 1,
        'username': 'test',
        'email': 'test@test.com',
    }


def test_read_users(client: TestClient):
    response = client.get('/users/')

    assert response.status_code == 200
    assert response.json() == {
        'users': [
            {
                'id': 1,
                'username': 'test',
                'email': 'test@test.com',
            },
        ],
    }


def test_update_user(client):
    response = client.put(
        '/users/1',
        json={
            'username': 'bob',
            'email': 'bob@test.com',
            'password': 'mynewpassword',
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        'id': 1,
        'username': 'bob',
        'email': 'bob@test.com',
    }


def test_delete_user(client):
    response = client.delete('/users/1')

    assert response.status_code == 200
    assert response.json() == {'detail': 'User deleted'}
