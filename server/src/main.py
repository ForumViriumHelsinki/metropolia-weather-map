import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from api.routes.analysis import analysis_router
from api.routes.graph_routes import graph_router
from api.routes.sensor_tags import sensor_tag_router
from api.routes.sensors import sensor_router
from api.routes.tags import tag_router
from cache import DATA_CACHE

# from utils.get_data_util import get_by_location

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
	yield


app = FastAPI(lifespan=lifespan)

origins = ["http://localhost:3000"]

app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)


@app.middleware("http")
async def log_request_info(request: Request, call_next):
	logger.info("GET %s", request.url.path)
	if request.query_params:
		for k, v in request.query_params.items():
			logger.info("%s - %s", k, v)

	response = await call_next(request)
	return response


@app.get("/api/test")
def test():
	print(DATA_CACHE.head())
	# get_by_location()
	return {"Hello"}


@app.get("/api")
def home():
	return {"This is the api home"}


@app.get("/update")
def update_hello():
	return {"message": "Global variable updated"}


app.include_router(sensor_router)
app.include_router(sensor_tag_router)
app.include_router(tag_router)
app.include_router(analysis_router)
app.include_router(graph_router)
