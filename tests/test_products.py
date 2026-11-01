from urllib import response


def test_create_product(client):
    response = client.post("/products/", json={
        "name": "Test Keyboard",
        "sku": "KEY-001",
        "quantity": 10,
        "price": 25.99
    })

    assert response.status_code == 201
    assert response.json["message"] == "Product added successfully"
    assert "product_id" in response.json

def test_get_all_products(client):
    client.post("/products/", json={
        "name": "Test Mouse",
        "sku": "MOU-001",
        "quantity": 15,
        "price": 12.50
    })

    response = client.get("/products/")

    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]["name"] == "Test Mouse"

def test_get_single_product(client):
    create_response = client.post("/products/", json={
        "name": "Test Monitor",
        "sku": "MON-001",
        "quantity": 5,
        "price": 150.00
    })

    product_id = create_response.json["product_id"]

    response = client.get(f"/products/{product_id}")

    assert response.status_code == 200
    assert response.json["name"] == "Test Monitor"

def test_update_product(client):
    create_response = client.post("/products/", json={
        "name": "Old Keyboard",
        "sku": "KEY-002",
        "quantity": 5,
        "price": 20.00
    })

    product_id = create_response.json["product_id"]

    response = client.put(f"/products/{product_id}", json={
        "name": "Updated Keyboard",
        "sku": "KEY-002",
        "quantity": 10,
        "price": 30.00
    })

    assert response.status_code == 200
    assert response.json["message"] == "Product updated successfully"

def test_delete_product(client):
    create_response = client.post("/products/", json={
        "name": "Test Headphones",
        "sku": "HEAD-001",
        "quantity": 8,
        "price": 45.00
    })

    product_id = create_response.json["product_id"]

    response = client.delete(f"/products/{product_id}")

    assert response.status_code == 200
    assert response.json["message"] == "Product deleted successfully"

def test_create_product_without_name(client):
    response = client.post("/products/", json={
        "sku": "TEST-003",
        "quantity": 5,
        "price": 20.00
    })

    assert response.status_code == 400

def test_create_product_with_negative_quantity(client):
    response = client.post("/products/", json={
        "name": "Test Speaker",
        "sku": "SPK-001",
        "quantity": -5,
        "price": 50.00
    })

    assert response.status_code == 400
def test_create_product_with_negative_price(client):
    response = client.post("/products/", json={
        "name": "Test Camera",
        "sku": "CAM-001",
        "quantity": 5,
        "price": -100.00
    })

    assert response.status_code == 400

def test_create_product_with_duplicate_sku(client):
    client.post("/products/", json={
        "name": "First Keyboard",
        "sku": "KEY-100",
        "quantity": 5,
        "price": 25.00
    })

    response = client.post("/products/", json={
        "name": "Second Keyboard",
        "sku": "KEY-100",
        "quantity": 10,
        "price": 30.00
    })

    assert response.status_code == 409