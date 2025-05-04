from src.utils.analysis_utils import (
	daily_avg_temp,
	filter_daytime_data,
	plot_daily_temp_avg,
	plot_monthly_temp_diff,
)
from src.utils.filter_tag import filter_location_with_tag
from src.utils.save_graph import save_graph


def avg_daily_temps_sun_shade():
	dfA = filter_location_with_tag("Vallila", "aurinko")
	dfA = filter_daytime_data(dfA)
	avg_sun = daily_avg_temp(dfA)

	dfV = filter_location_with_tag("Vallila", "varjo")
	dfV = filter_daytime_data(dfV)
	avg_shade = daily_avg_temp(dfV)

	plt1 = plot_daily_temp_avg(
		avg_sun,
		avg_shade,
		"Mäkelänkadun lämpötila auringossa ja varjossa",
		"Aurinko",
		"Varjo",
		"Päivämäärä",
		"°C",
		"orange",
		"royalblue",
	)
	save_graph("vallila_sun_shade_temp_diff", plt1, folder="vallila")

	plt2 = plot_monthly_temp_diff(
		dfA,
		dfV,
		"Mäkelänkadun lämpötilaero auringossa ja varjossa",
		ylim=(0, 1),
	)
	save_graph("vallila_sun_shade_monthly_temp_diff", plt2, folder="vallila")


if __name__ == "__main__":
	avg_daily_temps_sun_shade()
