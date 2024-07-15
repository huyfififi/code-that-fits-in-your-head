from datetime import datetime
from typing import Optional

from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    status,
)
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel

app = FastAPI()


# override the default status for malformed request payload 422 -> 400
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)


class Reservation(BaseModel):
    at: str
    email: str
    name: str
    quantity: int


class FakeDatabase:
    def __init__(self):
        self.collection = {"reservations": []}

    def post(self, reservation: Reservation) -> tuple[bool, Optional[str]]:
        # null validation is already done by Pydantic
        try:
            datetime.strptime(reservation.at, "%Y-%m-%d %H:%M")
        except ValueError:
            return False, f"malformed datetime {reservation.at}"

        self.collection["reservations"].append(reservation)
        return True, None


db = FakeDatabase()


def get_database() -> FakeDatabase:
    return db


@app.post(
    "/api/v1/reservations/",
    response_model=Reservation,
    status_code=status.HTTP_201_CREATED,
)
async def post_reservation(
    reservation: Reservation,
    db: FakeDatabase = Depends(get_database),
):
    success, err_msg = db.post(reservation)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=err_msg,
        )
    return reservation
