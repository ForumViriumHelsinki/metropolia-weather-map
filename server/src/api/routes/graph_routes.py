import asyncio

from fastapi import APIRouter, Query, Response

from analysis import (
    fluctuation_and_decomposition_analysis,
    humidity_delta_sun_vs_shade,
    location_analysis,
    temp_vs_humidity_correlation,
    temperature_delta_sun_vs_shade,
)

graph_router = APIRouter()


@graph_router.get("/api/plot/raw_humidity")
async def plot_raw_humidity():
    img_buffer = await asyncio.to_thread(
        fluctuation_and_decomposition_analysis.plot_raw_humidity
    )
    return Response(content=img_buffer.read(), media_type="image/png")


@graph_router.get("/api/plot/fft")
async def plot_fft(
    area: str = Query(
        None, description="Area to filter by (Vallila, Laajasalo, Koivukylä)"
    ),
):
    img_buffer = await asyncio.to_thread(
        fluctuation_and_decomposition_analysis.plot_fft_analysis, area
    )
    return Response(content=img_buffer.read(), media_type="image/png")


@graph_router.get("/api/plot/seasonal_decomposition")
async def plot_seasonal_decomposition():
    img_buffer = await asyncio.to_thread(
        fluctuation_and_decomposition_analysis.plot_seasonal_decomposition
    )
    return Response(content=img_buffer.read(), media_type="image/png")


@graph_router.get("/api/plot/humidity_delta")
async def plot_humidity_delta():
    img_buffer = await asyncio.to_thread(humidity_delta_sun_vs_shade.main)
    return Response(content=img_buffer.read(), media_type="image/png")


@graph_router.get("/api/plot/temperature_delta")
async def plot_temperature_delta():
    img_buffer = await asyncio.to_thread(temperature_delta_sun_vs_shade.main)
    return Response(content=img_buffer.read(), media_type="image/png")


@graph_router.get("/api/plot/humidity_trends")
async def plot_humidity_trends():
    img_buffer = await asyncio.to_thread(
        temp_vs_humidity_correlation.plot_humidity_trends
    )
    return Response(content=img_buffer.read(), media_type="image/png")


@graph_router.get("/api/plot/temp_vs_humidity_correlation")
async def plot_temp_vs_humidity_test():
    img_buffer = await asyncio.to_thread(
        temp_vs_humidity_correlation.plot_temp_vs_humidity
    )
    return Response(content=img_buffer.read(), media_type="image/png")


@graph_router.get("/api/plot/daily_temperature_range")
async def plot_daily_temperature_range():
    img_buffer = await asyncio.to_thread(
        location_analysis.plot_daily_temperature_range
    )
    return Response(content=img_buffer.read(), media_type="image/png")


@graph_router.get("/api/plot/daily_median_temperature")
async def plot_daily_median_temperature():
    img_buffer = await asyncio.to_thread(
        location_analysis.plot_daily_median_temperature
    )
    return Response(content=img_buffer.read(), media_type="image/png")


@graph_router.get("/api/plot/monthly_night_temperature")
async def plot_monthly_night_temperature():
    img_buffer = await asyncio.to_thread(
        location_analysis.plot_monthly_night_temperature
    )
    return Response(content=img_buffer.read(), media_type="image/png")


@graph_router.get("/api/plot/monthly_night_min_temperature")
async def plot_monthly_night_min_temperature():
    img_buffer = await asyncio.to_thread(
        location_analysis.plot_monthly_night_min_temperature
    )
    return Response(content=img_buffer.read(), media_type="image/png")


@graph_router.get("/api/plot/monthly_night_temperature_difference")
async def plot_monthly_night_temperature_difference():
    img_buffer = await asyncio.to_thread(
        location_analysis.plot_monthly_night_temperature_difference
    )
    return Response(content=img_buffer.read(), media_type="image/png")


@graph_router.get("/api/plot/daily_median_humidity")
async def plot_daily_median_humidity():
    img_buffer = await asyncio.to_thread(
        location_analysis.plot_daily_median_humidity
    )
    return Response(content=img_buffer.read(), media_type="image/png")


@graph_router.get("/api/plot/daily_humidity_range")
async def plot_daily_humidity_range():
    img_buffer = await asyncio.to_thread(
        location_analysis.plot_daily_humidity_range
    )
    return Response(content=img_buffer.read(), media_type="image/png")


@graph_router.get("/api/plot/day_night_humidity_difference")
async def plot_day_night_humidity_difference():
    img_buffer = await asyncio.to_thread(
        location_analysis.plot_day_night_humidity_difference
    )
    return Response(content=img_buffer.read(), media_type="image/png")


@graph_router.get("/api/plot/monthly_night_humidity")
async def plot_monthly_night_humidity():
    img_buffer = await asyncio.to_thread(
        location_analysis.plot_monthly_night_humidity
    )
    return Response(content=img_buffer.read(), media_type="image/png")
