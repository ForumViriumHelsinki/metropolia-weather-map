import SensorCard from "@/components/SensorCard";
import { Sensor } from "@/types";
import { apiFetch } from "@/utils/apiFetch";
export type LatestData = {
  id: string;
  properties: {
    measurement: {
      humidity: number;
      temperature: number;
      time: string;
    };
  };
};

export default async function Home() {
  const res = await apiFetch("/sensors");

  const sensors: Sensor[] = await res.json();
  // Sort sensors to have sensors in the sun to be displayed first
  const sortedSensors = sensors.sort((a) => {
    if (a.type === "Auringossa") {
      return -1;
    }
    if (a.type === "Varjossa") {
      return 1;
    }
    return 0;
  });

  const resLatest = await fetch(
    "https://bri3.fvh.io/opendata/makelankatu/makelankatu_latest.geojson",
  );
  const latestData = await resLatest.json();
  const dataList: LatestData[] = latestData.features;

  return (
    <main className="flex flex-col gap-6">
      <div className="h-96 w-full border-2"></div>

      <div className="grid gap-4 min-[720px]:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4">
        {sortedSensors.map((sensor) => (
          // <div
          // >
          <SensorCard
            key={sensor.id}
            sensor={sensor}
            latestData={dataList.filter((d) => d.id === sensor.id)[0]}
          />
          // </div>
        ))}
      </div>
    </main>
  );
}
