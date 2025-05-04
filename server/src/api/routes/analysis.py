import io
import re
from datetime import date, timedelta

from fastapi import APIRouter, HTTPException
from starlette.responses import StreamingResponse

from analysis.scripts.temperature_by_tag import temperature_by_tag

analysis_router = APIRouter()


@analysis_router.get("/api/analysis/temperature")
def get_temperature_graph(
	tag1: str,
	tag2: str,
	graph_type: str,
	location: str = None,
	start_date: str = None,
	end_date: str = None,
	time_of_day: str = "whole day",
):
	if graph_type == "plot" and start_date and end_date:
		start_date, end_date = parse_date(start_date, end_date)

	if graph_type == "bar" and start_date and end_date:
		start_date, end_date = parse_date(start_date, end_date)

	print("TIME OF DAY", time_of_day)

	daytime = False
	nighttime = False

	if time_of_day == "daytime":
		daytime = True
	elif time_of_day == "nighttime":
		nighttime = True

	try:
		graph = temperature_by_tag(
			tag1=tag1,
			tag2=tag2,
			location=location,
			graph_type=graph_type,
			start_date=start_date,
			end_date=end_date,
			daytime=daytime,
			nighttime=nighttime,
		)

		buf = io.BytesIO()
		graph.savefig(buf, format="svg")
		buf.seek(0)

		return StreamingResponse(buf, media_type="image/svg+xml")
	except Exception as e:
		print(e)


def parse_date(start_date, end_date):
	try:
		# YYYY-MM-DD
		if re.match(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", start_date) and re.match(
			r"[0-9]{4}-[0-9]{2}-[0-9]{2}", end_date
		):
			year, month, day = map(int, start_date.split("-"))
			parsed_start_date = date(year, month, day)

			year, month, day = map(int, end_date.split("-"))
			parsed_end_date = date(year, month, day)

		# YYYY-MM
		elif re.match(r"[0-9]{4}-[0-9]{2}", start_date) and re.match(
			r"[0-9]{4}-[0-9]{2}", end_date
		):
			year, month = map(int, start_date.split("-"))
			parsed_start_date = date(year, month, 1)

			year, month = map(int, end_date.split("-"))
			a = date(year, month + 1, 1)
			parsed_end_date = a - timedelta(days=1)

		else:
			raise ValueError(
				"Invalid date format. Expected YYYY-MM-DD or YYYY-MM."
			)

		return parsed_start_date, parsed_end_date

	except ValueError as ve:
		print(f"ValueError: {ve}")
		raise HTTPException(
			status_code=400, detail=f"Invalid date format: {ve}"
		)
	except Exception as e:
		print(f"Unexpected error: {e}")
		raise HTTPException(
			status_code=500,
			detail="An unexpected error occurred while parsing dates.",
		)
