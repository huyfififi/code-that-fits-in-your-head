from datetime import datetime
from typing import Optional, Union

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
    name: Union[str, None]  # FastAPI documents suggest Union instead of Optional
    quantity: int


class InsertResult:
    def __init__(
        self,
        success: bool = False,
        err_msg: Optional[str] = None,
        record=None,
    ):
        self.success = success
        self.err_msg = err_msg
        self.record = record


class FakeDatabase:
    def __init__(self):
        self.collection = {"reservations": []}

    def post(self, reservation: Reservation) -> tuple[bool, Optional[str]]:
        # null validation is already done by Pydantic

        try:
            datetime.strptime(reservation.at, "%Y-%m-%d %H:%M")
        except ValueError:
            return InsertResult(
                False,
                f"datetime {reservation.at} is malformed.",
                None,
            )
        if reservation.quantity <= 0:
            return InsertResult(False, "`quantity` must be greater than 0.", None)

        if reservation.name is None:
            reservation.name = ""

        self.collection["reservations"].append(reservation)
        return InsertResult(True, None, reservation)


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
    result = db.post(reservation)
    if not result.success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.err_msg,
        )
    return reservation
