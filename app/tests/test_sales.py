from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)
apiURL = "/sales/"

test_product = {
    "title": "Test",
    "cost": 200,
    "category_name": "Test",
    "materials": [
        {
            "material": {
                "title": "Test",
                "cost": 100,
                "measure": "grams"
            },
            "quantity": 1
        }
    ],
    "price": 500,
    "is_active": True,
    "is_compose": True
}

test_sale = {
    "details": [{
        "product": test_product,
        "quantity": 2
    }],
    "total": 1000
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

def delete(id):
    return client.delete(apiURL + str(id))

def test_read_sales():
    response = read_all()
    assert response.status_code == 200

def test_read_sale():
    response = read(19)
    assert response.status_code == 200
    assert response.json() == {
        "id": 19,
        "total": 50,
        "created_at": "2021-01-29T15:57:46.062216"
    }

def test_save_sale():
    response = save(test_sale)
    obj = response.json()
    assert response.status_code == 200
    delete(obj["id"])
    

def test_read_not_exsisting_sale():
    response = read(9999)
    assert response.status_code == 200
    assert response.json() == None
    
def test_create_existing_sale():
    obj = save(test_sale).json()
    response = save(test_sale)
    assert response.status_code == 400
    assert response.json() == {"detail": "Sale already registered"}
    delete(obj["id"])