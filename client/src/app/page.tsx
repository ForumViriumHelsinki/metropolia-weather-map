import DropMenu from "@/components/DropMenu";
import MapWrapper from "@/components/Map/MapWrapper";
import SensorCard from "@/components/SensorCard/SensorCard";
import VallilaCard from "@/components/SensorCard/VallilaCard";
import { Sensor } from "@/types";
import { apiFetch } from "@/utils/apiFetch";
import Analysis from "./(routes)/analysis/page";

export type VallilaLatestData = {
  id: string;
  properties: {
    measurement: {
      humidity: number;
      temperature: number;
      time: Date;
    };
  };
};

export interface LatestData {
  humidity: number;
  temperature: number;
  time: Date;
}

export default async function Home() {
  const res = await apiFetch("/sensors");
  const sensors: Sensor[] = await res.json();

  // Get latest data
  let latestData: VallilaLatestData[] = [];
  try {
    const resLatest = await fetch(
      "https://bri3.fvh.io/opendata/makelankatu/makelankatu_latest.geojson",
    );

    if (resLatest.status === 200) {
      const data = await resLatest.json();
      latestData = data.features;
    }
  } catch (error) {
    if (error instanceof Error) console.log(error.message);
  }

  const vallila = sensors.filter((s) => s.location === "Vallila");
  const koivukyla = sensors.filter((s) => s.location === "Koivukylä");
  const laajasalo = sensors.filter((s) => s.location === "Laajasalo");

  return (
    <main className="flex flex-col gap-6">
      {/* Map */}
      <div className="2xl:flex 2xl:gap-12">
        <h1 className="mb-2 text-5xl 2xl:pt-9">Mäkelänkatu</h1>
        <div className="2xl:w-fill aspect-2/3 w-full border-2 sm:aspect-2/1 2xl:aspect-2/1">
          <MapWrapper />
        </div>
      </div>

      {/* Sensor cards */}
      {!latestData && (
        <div className="text-xl text-red-800">
          Error fetching latest data from server
        </div>
      )}

      <DropMenu title="Vallila">
        {vallila.map((sensor) => {
          return (
            <VallilaCard
              key={sensor.id}
              sensor={sensor}
              latestData={
                latestData && latestData.filter((d) => d.id === sensor.id)[0]
              }
            />
          );
        })}
      </DropMenu>

      <DropMenu title="Koivukylä">
        {koivukyla.map((sensor) => (
          <SensorCard
            key={sensor.id}
            sensor={sensor}
            markerColor={"var(--color-shade)"}
          />
        ))}
      </DropMenu>

      <DropMenu title="Laajasalo">
        {laajasalo.map((sensor) => (
          <SensorCard
            key={sensor.id}
            sensor={sensor}
            markerColor={"var(--color-sun)"}
          />
        ))}
      </DropMenu>

      <Analysis />
    </main>
  );
}
