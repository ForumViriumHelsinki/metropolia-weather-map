from fastapi import FastAPI
from routes.sensor_routes import router as sensor_router
from routes.sensor_data_routes import router as sensor_data_router
from routes.analysis_route import router as analysis_router
from fastapi.middleware.cors import CORSMiddleware


# Create FastAPI instance
app = FastAPI()

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers for sensor related routes
app.include_router(sensor_router)

# Include routers for sensor data related routes
app.include_router(sensor_data_router)

app.include_router(analysis_router)


# Home route
@app.get("/")
def home():
    return {"message": "Hello, is anybody there?"}
