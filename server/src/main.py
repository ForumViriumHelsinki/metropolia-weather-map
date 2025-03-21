from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import router as routes
# from .sensor_repo import get_sensors # Depricated

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

@app.get("/api")
def home():
    return {"This is the api home"}

app.include_router(routes)

""" #Depricated
@app.get("/api/sensors")
async def test_get():
    sensors = await get_sensors()
    return sensors
"""
