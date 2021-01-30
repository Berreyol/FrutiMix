from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)
apiURL = "/product/inventory/"

test_product = {
    "title": "Test",
    "cost": 200,
    "category_name": "Test",
    "materials": [],
    "price": 500,
    "is_active": True,
    "is_compose": True
}

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

def test_read_inventory():
    response = read_all()
    assert response.status_code == 200

def test_read_inventory():
    response = read(1)
    assert response.status_code == 200
    assert response.json() == {
        "product_id": 1,
        "quantity": 10
    }

def test_save_inventory():
    response = save({
        "product": test_product,
        "quantity": 9999})
    response_obj = response.json()
    assert response.status_code == 200
    assert response_obj["product_id"] != None
    delete(response_obj["product_id"])

def test_update_inventory():
    obj = {
        "product": test_product,
        "quantity": 9999}
    obj = save(obj).json()
    test_obj = { 
        "product": test_product,
        "quantity": 1000}
    response = update(obj["product_id"], test_obj)
    assert response.status_code == 200
    assert response.json() != obj
    delete(obj["product_id"])

def test_delete_inventory():
    obj = {
        "product": test_product,
        "quantity": 9999}
    obj = save(obj).json()
    response = delete(obj["product_id"])
    assert response.status_code == 200
    assert response.json() == {"detail": "Inventory deleted successfully!"}

def test_read_not_exsisting_inventory():
    response = read(9999)
    assert response.status_code == 200
    assert response.json() == None
    
def test_create_existing_inventory():
    save({
        "product": test_product, 
        "quantity": 10
    })
    response = save({
        "product": test_product, 
        "quantity": 5
    })
    obj = response.json()
    assert response.status_code == 200
    assert obj["quantity"] == 15
    delete(obj["product_id"])

def test_update_not_existing_inventory():
    response = update(9999, {
        "product": test_product, 
        "quantity": 10})
    assert response.status_code == 400
    assert response.json() == {"detail": "Inventory doesn't exists"}

def test_delete_not_existing_inventory():
    response = delete(9999)
    assert response.status_code == 400
    assert response.json() == {"detail": "Inventory doesn't exists"}