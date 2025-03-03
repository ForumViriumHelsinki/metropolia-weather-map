from fastapi import FastAPI
from routes.sensor_routes import router as sensor_router
from routes.sensor_data_routes import router as sensor_data_router

app = FastAPI()

app.include_router(sensor_router)

app.include_router(sensor_data_router)

@app.get("/")
def home():
    return {"message": "Hello World"}

