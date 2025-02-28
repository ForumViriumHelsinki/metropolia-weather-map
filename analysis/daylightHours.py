import datetime
from astral.sun import sun
import csv

from astral import LocationInfo
city = LocationInfo("Helsinki", "Finland", "Europe/Helsinki", 60.19628790558516, 24.953944343215543)
print((
    f"Information for {city.name}/{city.region}\n"
    f"Timezone: {city.timezone}\n"
    f"Latitude: {city.latitude:.02f}; Longitude: {city.longitude:.02f}\n"
))

data = []

for m in range(1,13):
	for d in range(1,32):
		try:
			s = sun(city.observer, date=datetime.date(2024, m, d), tzinfo="Europe/Helsinki")
			data.append({"date": f"{d}/{m}", "sunrise": s["sunrise"], "sunset": s["sunset"]})
		except Exception as e:
			print(f"{d}/{m}")
			print(e)


with open('../data/daylight.csv', 'w', newline='') as csvfile:
	fieldNames = ["date", "sunrise", "sunset"]
	writer = csv.DictWriter(csvfile, fieldnames=fieldNames)
	writer.writeheader()
	writer.writerows(data)
