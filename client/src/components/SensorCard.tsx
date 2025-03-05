import { LatestData } from "@/app/page";
import { Sensor } from "@/types";

const SensorCard = ({
  sensor,
  latestData,
}: {
  sensor: Sensor;
  latestData: LatestData;
}) => {
  const idColor = sensor.type === "Auringossa" ? "#FFD580" : "#9370DB";
  const formatDate = (str: string) => {
    const date = str.slice(0, 10);
    const time = str.slice(11, 16);
    return `${date}  ${time}`;
  };

  return (
    <div className="flex flex-col gap-1 rounded-lg bg-offWhite px-4 py-3">
      <span
        className="inline-block w-full rounded-xl px-3 py-[2px] font-heavy"
        style={{ backgroundColor: idColor }}
      >
        {sensor.id.slice(-4)}
      </span>
      <h2 className="text-4xl">{sensor.type}</h2>

      <div className="flex flex-col">
        <span>
          Lämpötila: {latestData.properties.measurement.temperature}°C
        </span>
        <span>
          Ilmankosteus: {latestData.properties.measurement.temperature}%
        </span>
      </div>

      <h3 className="">Viimeisin mittaus</h3>
      <span>{formatDate(latestData.properties.measurement.time)}</span>

      <h3 className="">Sijainti</h3>
      <div>{sensor.attached}</div>
    </div>
  );
};

export default SensorCard;
