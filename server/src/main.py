from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .sensor_repo import get_sensors  # Use relative import

app = FastAPI()

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"Hello"}


@app.get("/api/sensors")
async def test_get():
    sensors = await get_sensors()
    return sensors
