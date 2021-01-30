from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)
apiURL = "/materials/"

def read_all():
    return client.get(apiURL)

def read(id):
    return client.get(apiURL + str(id))

def save(obj):
    return client.post(apiURL,
        headers = {"content-type": "application/json"},
        json = obj
    )

def update(id, obj):
    return client.put(apiURL + str(id),
        headers = {"content-type": "application/json"},
        json = obj
    )
def delete(id): 
    return client.delete(apiURL + str(id))

def test_read_materials():
    response = read_all()
    assert response.status_code == 200

def test_read_material():
    response = read(1)
    assert response.status_code == 200
    assert response.json() == {
        "cost": 100,
        "measure": "grams",
        "title": "Test",
        "id": 1
    }

def test_save_material():
    response = save({
        "title": "This is a save test",
        "measure": "string",
        "cost": 14})
    response_obj = response.json()
    assert response.status_code == 200
    assert response_obj["id"] != None
    delete(response_obj["id"])

def test_update_material():
    obj = {
        "title": "This is a update test",
        "measure": "string",
        "cost": 14}
    obj = save(obj).json()
    test_obj = { 
        "title": "This is a update title test",
        "measure": "string",
        "cost": 14}
    response = update(obj["id"], test_obj)
    assert response.status_code == 200
    assert response.json() != obj
    delete(obj["id"])

def test_delete_material():
    obj = {
        "title": "This is a delete test",
        "measure": "string",
        "cost": 14}
    obj = save(obj).json()
    response = delete(obj["id"])
    assert response.status_code == 200
    assert response.json() == {"detail": "Material deleted successfully!"}

def test_read_not_exsisting_material():
    response = read(9999)
    assert response.status_code == 200
    assert response.json() == None
    
def test_create_existing_material():
    response = save({
        "title": "Test", 
        "measure": "test",
        "cost": 0})
    assert response.status_code == 400
    assert response.json() == {"detail": "Material already registered"}

def test_update_not_existing_material():
    response = update(9999, {
        "title": "delete test",
        "measure": "delete test",
        "cost": 0})
    assert response.status_code == 400
    assert response.json() == {"detail": "Material doesn't exists"}

def test_delete_not_existing_material():
    response = delete(9999)
    assert response.status_code == 400
    assert response.json() == {"detail": "Material doesn't exists"}