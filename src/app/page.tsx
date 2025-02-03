import TestMap from "@/components/TestMap";

export default function Home() {
  return (
    <main className="flex flex-col w-screen h-screen justify-center items-center">
      <h1 className="inline text-2xl">Example map</h1>
      <div className="w-1/2 h-1/2 border">
        <TestMap />
      </div>
    </main>
  );
}
