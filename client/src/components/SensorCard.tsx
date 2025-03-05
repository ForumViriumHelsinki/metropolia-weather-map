import { Sensor } from "@/types";

type LatestData = {
  id: string;
  properties: {
    measurement: {
      humidity: number;
      temperature: number;
      time: string;
    };
  };
};

const SensorCard = ({
  sensor,
  latestData,
}: {
  sensor: Sensor;
  latestData: LatestData;
}) => {
  return (
    <div className="bg-offWhite border-2">
      <span>{sensor.id.slice(-4)}</span>
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
      <span>{latestData.properties.measurement.time.substring(0, 10)}</span>

      <h3 className="">Sijainti</h3>
      <div>{sensor.attached}</div>
    </div>
  );
};

export default SensorCard;
