"use client";
import { apiFetch } from "@/utils/apiFetch";
import { useState } from "react";

export default function Home() {
  const [images, setImages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [fetchedEndpoints, setFetchedEndpoints] = useState(new Set()); // Track fetched endpoints!

  const endpoints = [
    "/plot/raw_humidity",
    "/plot/fft",
    "/plot/fft?area=Vallila",
    "/plot/fft?area=Laajasalo",
    "/plot/fft?area=Koivukyla",
    "/plot/seasonal_decomposition",
    "/plot/humidity_delta",
    "/plot/temperature_delta",
    "/plot/humidity_trends",
    "/plot/temp_vs_humidity_correlation",
    "/plot/daily_temperature_range",
    "/plot/daily_median_temperature",
    "/plot/monthly_night_temperature",
    "/plot/monthly_night_min_temperature",
    "/plot/monthly_night_temperature_difference",
    "/plot/daily_median_humidity",
    "/plot/daily_humidity_range",
    "/plot/day_night_humidity_difference",
    "/plot/monthly_night_humidity",
  ];

  // Function to fetch all images from the API (currently not in use)
  const LoadAllImages = async () => {
    setLoading(true);

    try {
      const endpointsToFetch = endpoints.filter(
        (endpoint) => !fetchedEndpoints.has(endpoint),
      );
      const fetches = endpointsToFetch.map((endpoint) =>
        apiFetch(endpoint).then((res) => res.blob()),
      );
      const blobs = await Promise.all(fetches);

      const imageObjectUrls = blobs.map((blob) => URL.createObjectURL(blob));

      setImages((prevImages) => [...prevImages, ...imageObjectUrls]);
      setFetchedEndpoints((prev) => {
        const updated = new Set(prev);
        endpointsToFetch.forEach((endpoint) => updated.add(endpoint));
        return updated;
      });
    } catch (error) {
      console.error("Error fetching images:", error);
    } finally {
      setLoading(false);
    }
  };
  // Function to fetch a single image from the API
  const LoadImage = async (endpoint) => {
    if (fetchedEndpoints.has(endpoint)) {
      console.log(`Already fetched: ${endpoint}`);
      return; // Don't fetch again
    }

    setLoading(true);

    try {
      const res = await apiFetch(endpoint);
      const blob = await res.blob();
      const imageObjectUrl = URL.createObjectURL(blob);

      setImages((prevImages) => [...prevImages, imageObjectUrl]);
      setFetchedEndpoints((prev) => {
        const updated = new Set(prev);
        updated.add(endpoint);
        return updated;
      });
    } catch (error) {
      console.error("Error fetching image:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="flex flex-col gap-6">
      <h1 className="mb-2 text-5xl">Graphs</h1>
      <div className="flex flex-wrap gap-6">
        <button
          onClick={LoadAllImages}
          className="rounded bg-blue-500 px-4 py-2 text-white hover:bg-blue-600"
        >
          {loading ? "Loading..." : "Load Graphs"}
        </button>
        {endpoints.map((endpoint) => (
          <button
            key={endpoint}
            onClick={() => LoadImage(endpoint)}
            className="rounded bg-blue-500 px-4 py-2 text-white hover:bg-blue-600"
          >
            Load {endpoint}
          </button>
        ))}
      </div>

      <div className="flex flex-col gap-6">
        {images.map((imgSrc, index) => (
          <img
            key={index}
            src={imgSrc}
            alt={`Image ${index}`}
            className="h-auto w-auto rounded shadow"
          />
        ))}
      </div>
    </main>
  );
}
