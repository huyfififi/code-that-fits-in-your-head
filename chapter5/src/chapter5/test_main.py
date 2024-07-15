import pydantic
import pytest
from fastapi import status
from fastapi.testclient import TestClient

from .main import app, Reservation

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
        {
            "at": "2023-08-23 16:55",
            "email": "kite@example.edu",
            "name": None,
            "quantity": 2,
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
        {
            "at": "not a date",
            "email": "w@example.edu",
            "name": "Wk Hd",
            "quantity": 8,
        },
        {
            "at": "2023-11-30 20:01",
            "email": None,
            "name": "Thora",
            "quantity": 19,
        },
        {
            "at": "2022-01-02 12:10",
            "email": "3@example.org",
            "name": "3 Beard",
            "quantity": 0,
        },
        {
            "at": "2045-12-31 11:45",
            "email": "git@example.com",
            "name": "Gil Tan",
            "quantity": -1,
        },
    ]
    for data in test_data:
        response = client.post("/api/v1/reservations", json=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_quaitity_must_be_positive():
    test_data = [0, -1]  # boundary testing
    for invalid_quantity in test_data:
        with pytest.raises(pydantic.ValidationError):
            Reservation(
                **{
                    "at": "2024-08-19 11:30",
                    "email": "mail@example.com",
                    "name": "Marie Ilsoe",
                    "quantity": invalid_quantity,
                }
            )
