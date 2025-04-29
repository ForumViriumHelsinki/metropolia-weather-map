from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes.analysis import analysis_router
from src.api.routes.sensor_tags import sensor_tag_router
from src.api.routes.sensors import sensor_router
from src.api.routes.tags import tag_router
from src.api.routes.graph_routes import graph_router

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


app.include_router(sensor_router)
app.include_router(sensor_tag_router)
app.include_router(tag_router)
app.include_router(analysis_router)
app.include_router(graph_router)
