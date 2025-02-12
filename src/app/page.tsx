import SensorInfo from "@/components/SensorInfo";
import tempData from "./temp-data.json";

export type TempData = {
  type: string;
  temperature: number;
  humidity: number;
  attached: string;
};

export default async function Home() {
  const tData = tempData;

  return (
    <main className="flex flex-col gap-12">
      {/* Hero */}
      <div className="flex w-full justify-between bg-yellow-pale px-[16.666%] dark:bg-dark-banner">
        <h1 className="w-1/4 pt-9 text-5xl">Mäkelänkatu</h1>
        <div className="aspect-[2/1] w-1/2 border-2">{/* <TestMap /> */}</div>
      </div>

      {/* Sensor data */}
      <div className="mx-auto w-4/6">
        <h2 className="mb-4 block text-4xl">Sensorit</h2>
        <div className="grid grid-cols-5 gap-6">
          {tData.map((d, index) => (
            <div
              key={index}
              // Dynamically created Tailwind classes don't work here
              style={{
                position: "relative",
                zIndex: -Math.floor(index / 5) + 999,
              }}
            >
              <SensorInfo data={d} />
            </div>
          ))}
        </div>
      </div>
    </main>
  );
}
