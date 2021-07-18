import json

from aki.app import app


def test_heart_route():
    client = app.test_client()
    url = '/'

    response = client.get(url)
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data['lavanderia'] == 'aki'


def test_add_employee():
    with app.test_client() as client:
        response = client.post(
            '/empleados/nuevo/',
            data=json.dumps(dict(
                first_name="john", last_name="gato", document="55111111"
            )),
            content_type="application/json",
        )
        data = json.loads(response.data.decode())
        assert response.status_code == 200
        assert 'success' in data['status']


def test_invalid_exists_employee():
    with app.test_client() as client:
        response = client.post(
            '/empleados/nuevo/',
            data=json.dumps(dict(
                first_name="john", last_name="gato", document="55111111"
            )),
            content_type="application/json",
        )
        data = json.loads(response.data.decode())
        assert response.status_code == 200
        assert 'error' in data['status']


def test_list_employee():
    client = app.test_client()
    url = '/empleados/'

    response = client.get(url)
    data = json.loads(response.data)
    assert response.status_code == 200
    assert 'success' in data['status']
    assert len(data['employees']) > 0
