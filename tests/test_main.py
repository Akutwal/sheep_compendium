# test_main.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_read_sheep():
    response = client.get("/sheep/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Spice",
        "breed": "Gotland",
        "sex": "ewe"
    }


def test_add_sheep():
    new_sheep_data = {
        "id": 7,
        "name": "Woolsey",
        "breed": "Merino",
        "sex": "ram"
    }
    response = client.post("/sheep/", json=new_sheep_data)
    assert response.status_code == 201
    assert response.json() == new_sheep_data

    verify_response = client.get(f"/sheep/{new_sheep_data['id']}")
    assert verify_response.json() == new_sheep_data


def test_delete_sheep():
    # First create a sheep to delete
    test_sheep = {
        "id": 8,
        "name": "DeleteMe",
        "breed": "Suffolk",
        "sex": "ram"
    }
    client.post("/sheep/", json=test_sheep)

    # Delete the sheep
    response = client.delete(f"/sheep/{test_sheep['id']}")
    assert response.status_code == 204

    # Verify sheep is deleted
    verify_response = client.get(f"/sheep/{test_sheep['id']}")
    assert verify_response.status_code == 404


def test_update_sheep():
    # First create a sheep to update
    original_sheep = {
        "id": 9,
        "name": "Original",
        "breed": "Merino",
        "sex": "ewe"
    }
    client.post("/sheep/", json=original_sheep)

    # Update the sheep
    updated_sheep = {
        "id": 9,
        "name": "Updated",
        "breed": "Suffolk",
        "sex": "ewe"
    }
    response = client.put(f"/sheep/{updated_sheep['id']}", json=updated_sheep)
    assert response.status_code == 200
    assert response.json() == updated_sheep

    # Verify update persisted
    verify_response = client.get(f"/sheep/{updated_sheep['id']}")
    assert verify_response.json() == updated_sheep


def test_read_all_sheep():
    # Add test sheep if needed
    test_sheep1 = {
        "id": 10,
        "name": "Sheep1",
        "breed": "Merino",
        "sex": "ewe"
    }
    test_sheep2 = {
        "id": 11,
        "name": "Sheep2",
        "breed": "Suffolk",
        "sex": "ram"
    }
    client.post("/sheep/", json=test_sheep1)
    client.post("/sheep/", json=test_sheep2)

    # Get all sheep
    response = client.get("/sheep/")
    assert response.status_code == 200
    sheep_list = response.json()

    # Verify the test sheep are in the list
    assert any(sheep["id"] == test_sheep1["id"] for sheep in sheep_list)
    assert any(sheep["id"] == test_sheep2["id"] for sheep in sheep_list)