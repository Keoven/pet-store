from unittest import mock

import pytest

from ..utils import seed_database


def test_ping(client):
    response = client.get('/healthcheck')
    assert response.status_code == 204


def test_pet_should_return_json_response(client):
    response = client.get('/pet')
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response.json() == []


def test_pet_should_create_new_pet(client, species):
    response = client.post('/pet', json={
        'name': 'Bob',
        'age': 3,
        'species': species.id,
    })

    assert response.status_code == 201
    assert response.headers['Content-Type'] == 'application/json'
    assert response.json() == {
        'id': mock.ANY,
        'name': 'Bob',
        'age': 3,
        'species': mock.ANY,
        'updated_at': mock.ANY,
        'created_at': mock.ANY,
    }

    response = client.get('/pet')
    response_json = response.json()
    assert len(response_json) == 1
    assert response_json[0]['name'] == 'Bob'


def test_pet_should_not_allow_unknown_species(client, species):
    response = client.post('/pet', json={
        'name': 'Bob',
        'age': 3,
        'species': 'unknown_species',
    })
    assert response.status_code == 422


def test_should_not_allow_empty_name(client, species):
    response = client.post('/pet', json={
        'name': '',
        'age': 3,
        'species': species.id,
    })
    assert response.status_code == 422


@pytest.mark.parametrize('age', ['', 0, -1, 1.5])
def test_should_not_allow_invalid_age(client, species, age):
    response = client.post('/pet', json={
        'name': '',
        'age': '',
        'species': species.id,
    })
    assert response.status_code == 422


def test_should_filter_by_name(client, species, db_session):
    seed_database(db_session)
    response = client.get('/pet?name=abe')
    assert response.status_code == 200
    assert len(response.json()) == 3


def test_should_filter_by_species(client, species, db_session):
    seed_database(db_session)
    response = client.get('/pet?species=cat')
    assert response.status_code == 200
    assert len(response.json()) == 42


def test_should_filter_by_age(client, species, db_session):
    seed_database(db_session)
    response = client.get('/pet?age=5')
    assert response.status_code == 200
    assert len(response.json()) == 7


@pytest.mark.parametrize(
    'path, count',
    [
        ('/pet?name=abe&species=dog&age=7', 1),
        ('/pet?name=abe&species=cat&age=6', 0),
    ]
)
def test_should_filter_in_combination(client, species, db_session, path, count):
    seed_database(db_session)
    response = client.get(path)
    assert response.status_code == 200
    assert len(response.json()) == count
