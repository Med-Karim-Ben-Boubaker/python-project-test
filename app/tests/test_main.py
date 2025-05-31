def test_read_root(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the FastAPI CI/CD Demo"}

def test_create_and_read_item(test_client):
    # Test creating an item
    item_data = {"name": "Test Item", "description": "A test item", "price": 9.99, "tax": 1.0}
    response = test_client.post("/items/", json=item_data)
    assert response.status_code == 200
    assert response.json()["name"] == "Test Item"
    
    # Test reading the created item
    item_id = 1  # First item should have ID 1
    response = test_client.get(f"/items/{item_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Test Item"

def test_read_nonexistent_item(test_client):
    response = test_client.get("/items/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"

def test_health_check(test_client):
    response = test_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
