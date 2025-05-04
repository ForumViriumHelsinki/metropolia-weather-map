import sys
import time

import pandas as pd

from src.utils.get_data_util import get_all_locations

start_time = time.time()
big_data = get_all_locations()
print("Fetch time --- %s seconds ---" % (time.time() - start_time))

sys.exit("Hello")
# Save and read in different formats
formats = {
	"csv": "big_data.csv",
	"json": "big_data.json",
	"parquet": "big_data.parquet",
}

for fmt, filename in formats.items():
	# Save the data
	if fmt == "csv":
		big_data.to_csv(filename, index=False)
	elif fmt == "json":
		big_data.to_json(filename, orient="records", lines=True)
	elif fmt == "parquet":
		big_data.to_parquet(filename, index=False)

	# Read the data and measure time
	start_time = time.time()
	if fmt == "csv":
		data = pd.read_csv(filename)
	elif fmt == "json":
		data = pd.read_json(filename, orient="records", lines=True)
	elif fmt == "parquet":
		data = pd.read_parquet(filename)
	elif fmt == "hdf":
		data = pd.read_hdf(filename, key="df")
	print(f"Reading {fmt} took --- %s seconds ---" % (time.time() - start_time))
