from fastapi import APIRouter, Query, Response

from ...utils.utils import map_locations

from ...analysis import fluctuation_and_decomposition_analysis
from ...analysis import humidity_delta_sun_vs_shade
from ...analysis import temperature_delta_sun_vs_shade
from ...analysis import temp_vs_humidity_correlation


graph_router = APIRouter()

@graph_router.get("/api/plot/raw_humidity")
async def plot_raw_humidity():
    img_buffer = fluctuation_and_decomposition_analysis.plot_raw_humidity()
    return Response(content=img_buffer.read(), media_type="image/png")

@graph_router.get("/api/plot/fft")
async def plot_fft():
    img_buffer = fluctuation_and_decomposition_analysis.plot_fft_analysis()
    return Response(content=img_buffer.read(), media_type="image/png")

@graph_router.get("/api/plot/seasonal_decomposition")
async def plot_seasonal_decomposition():
    img_buffer = fluctuation_and_decomposition_analysis.plot_seasonal_decomposition()
    return Response(content=img_buffer.read(), media_type="image/png")

@graph_router.get("/api/plot/humidity_delta")
async def plot_humidity_delta():
    img_buffer = humidity_delta_sun_vs_shade.main()
    return Response(content=img_buffer.read(), media_type="image/png")

@graph_router.get("/api/plot/temperature_delta")
async def plot_temperature_delta():
    img_buffer = temperature_delta_sun_vs_shade.main()
    return Response(content=img_buffer.read(), media_type="image/png")

@graph_router.get("/api/plot/humidity_trends")
async def plot_humidity_trends():
    img_buffer = temp_vs_humidity_correlation.plot_humidity_trends()
    return Response(content=img_buffer.read(), media_type="image/png")

@graph_router.get("/api/plot/temp_vs_humidity_correlation")
async def plot_temp_vs_humidity_test():
    img_buffer = temp_vs_humidity_correlation.plot_temp_vs_humidity()
    return Response(content=img_buffer.read(), media_type="image/png")
