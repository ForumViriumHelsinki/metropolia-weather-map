import TestMap from "@/components/TestMap";

export default function Home() {
  return (
    <main className="flex h-screen w-screen flex-col items-center justify-center">
      <h1 className="inline text-2xl">Example map</h1>
      <div className="h-1/2 w-1/2 border">
        <TestMap />
      </div>
    </main>
  );
}
