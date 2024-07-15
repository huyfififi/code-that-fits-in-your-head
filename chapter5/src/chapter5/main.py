from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI()


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
