from fastapi import status
from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_post_valid_reservation_when_database_is_empty():
    test_data = [
        {
            "at": "2023-11-24 19:00",
            "email": "juliad@example.net",
            "name": "Julia Domna",
            "quantity": 5,
        },
        {
            "at": "2024-02-13 18:15",
            "email": "x@example.com",
            "name": "Xenia Ng",
            "quantity": 9,
        },
    ]
    for data in test_data:
        response = client.post("/api/v1/reservations", json=data)
        assert response.status_code == status.HTTP_201_CREATED


def test_post_invalid_reservation():
    test_data = [
        {
            "at": None,
            "email": "j@example.net",
            "name": "Jay Xerxes",
            "quantity": 1,
        },
    ]
    for data in test_data:
        response = client.post("/api/v1/reservations", json=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
