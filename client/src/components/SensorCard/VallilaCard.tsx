import { VallilaLatestData } from "@/app/page";
import { Sensor } from "@/types";
import { formatDate } from "@/utils/formatDate";

const VallilaCard = async ({
  sensor,
  latestData,
}: {
  sensor: Sensor;
  latestData: VallilaLatestData;
}) => {
  return (
    <div className="card-padding-border bg-off-white">
      <span className="font-heavy py-[2px], bg-green-leaf inline-block w-full rounded-xl px-3">
        {sensor.id.slice(-4)}
      </span>
      <div>
        <h2 className="text-3xl">{sensor.location}</h2>

        <div className="flex flex-col">
          <span>
            Lämpötila: {latestData.properties.measurement.temperature || "-"}°C
          </span>
          <span>
            Ilmankosteus: {latestData.properties.measurement.temperature || "-"}
            %
          </span>
        </div>
      </div>

      <div>
        <h3>Viimeisin mittaus</h3>
        <span>{formatDate(latestData.properties.measurement.time) || "-"}</span>
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

export default VallilaCard;
