from fastapi import FastAPI, status
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


@app.post(
    "/api/v1/reservations/",
    response_model=Reservation,
    status_code=status.HTTP_201_CREATED,
)
async def post_reservation(reservation: Reservation):
    return reservation
