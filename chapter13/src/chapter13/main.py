import time
import functools

from pydantic import BaseModel


logs = []


def log_decorator(method):
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        result: Reservation = method(*args, **kwargs)
        logs.append(
            {
                "timestamp": time.time(),
                "reservation": result.model_dump(),
            }
        )
        return result

    return wrapper


class Reservation(BaseModel):
    guid: int
    at: str
    email: str
    name: str
    quantity: int


class IReservationsRepository:
    fake_db = [
        {
            "guid": 1,
            "at": "2024-07-20 18:00",
            "email": "geohot@example.com",
            "name": "George Hotz",
            "quantity": 1,
        },
        {
            "guid": 2,
            "at": "2024-07-20 19:00",
            "email": "linus@example.com",
            "name": "Linus Torvals",
            "quantity": 4,
        },
        {
            "guid": 3,
            "at": "2024-07-21 20:00",
            "email": "bill@example.com",
            "name": "Bill Joy",
            "quantity": 5,
        },
    ]

    @log_decorator
    def read_reservation(self, guid: int) -> Reservation:
        """return a dummy reservation"""
        for rec in self.fake_db:
            if rec["guid"] != guid:
                continue
            return Reservation(**rec)
        raise NotImplementedError("record not found")


def test_log_read_reservations(mocker):
    repo = IReservationsRepository()
    mocker.patch("time.time", return_value=1.0)
    repo.read_reservation(1)

    mocker.patch("time.time", return_value=2.0)
    repo.read_reservation(2)

    mocker.patch("time.time", return_value=3.0)
    repo.read_reservation(1)

    mocker.patch("time.time", return_value=4.0)
    repo.read_reservation(3)

    assert logs[0]["reservation"]["guid"] == 1
    assert logs[0]["timestamp"] == 1.0

    assert logs[1]["reservation"]["guid"] == 2
    assert logs[1]["timestamp"] == 2.0

    assert logs[2]["reservation"]["guid"] == 1
    assert logs[2]["timestamp"] == 3.0

    assert logs[3]["reservation"]["guid"] == 3
    assert logs[3]["timestamp"] == 4.0
