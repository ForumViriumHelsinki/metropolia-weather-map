import SensorCard from "@/components/SensorCard";
import { Sensor } from "@/types";
import { apiFetch } from "@/utils/apiFetch";

export default async function Home() {
  // await testGetAction();
  const res = await apiFetch("/sensors");
  const sensors: Sensor[] = await res.json();

  const resLatest = await fetch(
    "https://bri3.fvh.io/opendata/makelankatu/makelankatu_latest.geojson",
  );
  const latestData = await resLatest.json();
  const dataList = latestData.features;
  const testData = dataList.filter((d: any) => d.id === sensors[0].id)[0];
  // const tempLatest = latestData;

  return (
    <main className="flex flex-col gap-6">
      <div className="h-96 w-full border-2"></div>
      <SensorCard
        sensor={sensors[0]}
        latestData={testData}
      />
    </main>
  );
}
