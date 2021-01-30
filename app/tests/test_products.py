from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)
apiURL = "/products/"

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

def test_read_products():
    response = read_all()
    assert response.status_code == 200

def test_read_product():
    response = read(1)
    assert response.status_code == 200
    assert response.json() == {
        "price": 20,
        "category_name": "Test",
        "materials": [],
        "is_active": True,
        "cost": 10,
        "title": "Refresco",
        "is_compose": False
    }

def test_save_product():
    response = save({
        "price": 20,
        "category_name": "Test",
        "is_active": True,
        "materials": [],
        "cost": 10,
        "title": "This is a save test",
        "is_compose": True})
    response_obj = response.json()
    assert response.status_code == 200
    assert response_obj["id"] != None
    delete(response_obj["id"])

def test_update_product():
    obj = {
        "price": 20,
        "category_name": "Test",
        "is_active": True,
        "materials": [],
        "cost": 10,
        "title": "This is a update test",
        "is_compose": True}
    obj = save(obj).json()
    test_obj = { 
        "price": 20,
        "category_name": "Test",
        "is_active": True,
        "materials": [],
        "cost": 10,
        "title": "This is a updated title test",
        "is_compose": True}
    response = update(obj["id"], test_obj)
    assert response.status_code == 200
    assert response.json() != obj
    delete(obj["id"])

def test_delete_product():
    obj = {
        "price": 20,
        "category_name": "Test",
        "is_active": True,
        "materials": [],
        "cost": 10,
        "title": "This is a delete test",
        "is_compose": True}
    obj = save(obj).json()
    response = delete(obj["id"])
    assert response.status_code == 200
    assert response.json() == {"detail": "Product deleted successfully!"}

def test_read_not_exsisting_product():
    response = read(9999)
    assert response.status_code == 200
    assert response.json() == None
    
def test_create_existing_product():
    response = save({
        "price": 20,
        "category_name": "Test",
        "is_active": True,
        "materials": [],
        "cost": 10,
        "title": "Refresco",
        "is_compose": False})
    assert response.status_code == 400
    assert response.json() == {"detail": "Product already registered"}

def test_update_not_existing_product():
    response = update(9999, {
        "price": 20,
        "category_name": "Test",
        "materials": [],
        "is_active": True,
        "cost": 10,
        "title": "This is a delete test",
        "is_compose": True})
    assert response.status_code == 400
    assert response.json() == {"detail": "Product doesn't exists"}

def test_delete_not_existing_product():
    response = delete(9999)
    assert response.status_code == 400
    assert response.json() == {"detail": "Product doesn't exists"}