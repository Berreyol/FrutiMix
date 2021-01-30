from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)
apiURL = "/categories/"

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

def test_read_categories():
    response = read_all()
    assert response.status_code == 200

def test_read_category():
    response = read(4)
    assert response.status_code == 200
    assert response.json() == {
        "name": "Test",
        "description": "This is a category test",
        "id": 4
    }

def test_save_category():
    response = save({
        "name": "This is a save test",
        "description": "test"})
    response_obj = response.json()
    assert response.status_code == 200
    assert response_obj["id"] != None
    delete(response_obj["id"])

def test_update_category():
    obj = {
        "name": "This is a update test",
        "description": "test"}
    obj = save(obj).json()
    test_obj = { 
        "name": "This is a update name test",
        "description": "test"}
    response = update(obj["id"], test_obj)
    assert response.status_code == 200
    assert response.json() != obj
    delete(obj["id"])

def test_delete_category():
    obj = {
        "name": "This is a delete test",
        "description": "test"}
    obj = save(obj).json()
    response = delete(obj["id"])
    assert response.status_code == 200
    assert response.json() == {"detail": "Category deleted successfully!"}

def test_read_not_exsisting_category():
    response = read(9999)
    assert response.status_code == 200
    assert response.json() == None
    
def test_create_existing_category():
    response = save({
        "name": "Test", 
        "description": "test"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Category already registered"}

def test_update_not_existing_category():
    response = update(9999, {
        "name": "delete test",
        "description": "test"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Category doesn't exists"}

def test_delete_not_existing_category():
    response = delete(9999)
    assert response.status_code == 400
    assert response.json() == {"detail": "Category doesn't exists"}