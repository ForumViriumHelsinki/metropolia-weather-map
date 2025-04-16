import { LatestData } from "@/app/page";
import { Sensor } from "@/types";
import { formatDate } from "@/utils/formatDate";

const SensorCard = async ({
  sensor,
  markerColor,
}: {
  sensor: Sensor;
  markerColor: string;
}) => {
  const res = await fetch(sensor.csv_link);
  const rawData = await res.json();
  const measurements = rawData.properties.data.raw;
  const latestData: LatestData = measurements[measurements.length - 1];

  return (
    <div className="card-padding-border bg-off-white">
      <span
        className="font-heavy inline-block w-full rounded-xl px-3 py-[2px]"
        style={{ backgroundColor: markerColor }}
      >
        {sensor.id.slice(-4)}
      </span>
      <div>
        <h2 className="text-3xl">{sensor.location}</h2>

        <div className="flex flex-col">
          <span>Lämpötila: {latestData.temperature}°C</span>
          <span>Ilmankosteus: {latestData.humidity}%</span>
        </div>
      </div>

      <div>
        <h3>Viimeisin mittaus</h3>
        <span>{formatDate(latestData.time)}</span>
      </div>

      <div>
        <h3>Data</h3>
        <a
          href={sensor.csv_link}
          target="_blank"
        >
          geojson
        </a>
      </div>
    </div>
  );
};

export default SensorCard;
