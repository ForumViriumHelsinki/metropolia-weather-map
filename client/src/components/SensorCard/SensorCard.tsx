import { LatestData } from "@/app/page";
import { Sensor } from "@/types";
import { fixLocation } from "@/utils/fixLocation";

const SensorCard = ({
  sensor,
  latestData,
}: {
  sensor: Sensor;
  latestData: LatestData;
}) => {
  const idColor = "var(--color-green-leaf)";

  const formatDate = (str: string) => {
    const date = str.slice(0, 10);
    const time = str.slice(11, 16);
    return `${time} - ${date}`;
  };
  const valid = !!latestData;

  return (
    <div className="card-padding-border bg-off-white">
      <span
        className="font-heavy inline-block w-full rounded-xl px-3 py-[2px]"
        style={{ backgroundColor: idColor }}
      >
        {sensor.id.slice(-4)}
      </span>
      <div>
        <h2 className="text-3xl">{fixLocation(sensor.location)}</h2>

        <div className="flex flex-col">
          <span>
            Lämpötila:{" "}
            {valid ? latestData.properties.measurement.temperature : "-"}°C
          </span>
          <span>
            Ilmankosteus:{" "}
            {valid ? latestData.properties.measurement.temperature : "-"}%
          </span>
        </div>
      </div>

      <div>
        <h3>Viimeisin mittaus</h3>
        <span>
          {valid ? formatDate(latestData.properties.measurement.time) : "-"}
        </span>
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
