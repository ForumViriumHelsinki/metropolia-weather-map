"use client";
import { apiFetch } from "@/utils/apiFetch";
import { useState } from "react";
import toast from "react-hot-toast";

export default function GraphsLoader() {
  const [images, setImages] = useState<
    { url: string; endpoint: string; visible: boolean }[]
  >([]);
  const [loading, setLoading] = useState(false);
  const [fetchedEndpoints, setFetchedEndpoints] = useState(new Set()); // Track fetched endpoints!

  const endpoints = [
    ["/plot/raw_humidity", "Raaka kosteusdata"],
    ["/plot/fft", "FFT"],
    ["/plot/fft?area=Vallila", "FFT Vallilasta"],
    ["/plot/fft?area=Laajasalo", "FFT Laajasalosta"],
    ["/plot/fft?area=Koivukyl%C3%A4", "FFT Koivukylästä"],
    ["/plot/seasonal_decomposition", "Kausivaihtelun purku"],
    ["/plot/humidity_delta", "Kosteuden muutos"],
    ["/plot/temperature_delta", "Lämpötilan muutos"],
    ["/plot/humidity_trends", "Kosteuden trendit"],
    [
      "/plot/temp_vs_humidity_correlation",
      "Lämpötilan ja kosteuden korrelaatio",
    ],
    ["/plot/daily_temperature_range", "Päivittäinen lämpötilaero"],
    ["/plot/daily_median_temperature", "Päivittäinen keskilämpötila"],
    ["/plot/monthly_night_temperature", "Kuukausittainen yölämpötila"],
    ["/plot/monthly_night_min_temperature", "Kuukausittainen minimilämpötila"],
    [
      "/plot/monthly_night_temperature_difference",
      "Kuukausittainen yölämpötilaero",
    ],
    ["/plot/daily_median_humidity", "Päivittäinen kosteuden mediaani"],
    ["/plot/daily_humidity_range", "Päivittäinen kosteusero"],
    ["/plot/day_night_humidity_difference", "Yön ja päivän kosteusero"],
    ["/plot/monthly_night_humidity", "Kuukausittainen yökosteus"],
  ];

  const LoadAllImages = async () => {
    setLoading(true);

    try {
      const endpointsToFetch = endpoints.filter(
        (endpoint) => !fetchedEndpoints.has(endpoint),
      );
      const fetches = endpointsToFetch.map((endpoint) =>
        apiFetch(endpoint[0])
          .then((res) => res.blob())
          .then((blob) => ({
            url: URL.createObjectURL(blob),
            endpoint: endpoint[0],
            visible: true,
          })),
      );
      
      const imageObjects = await Promise.all(fetches);
      setImages((prevImages) => [...prevImages, ...imageObjects]);
     
      setFetchedEndpoints((prev) => {
        const updated = new Set(prev);
        endpointsToFetch.forEach((endpoint) => updated.add(endpoint[0]));
        return updated;
      });
    } catch (error) {
      console.error("Error fetching images:", error);
    } finally {
      setLoading(false);
    }
  };

  const LoadImage = async (endpoint: string) => {
    const existing = images.find((img) => img.endpoint === endpoint);
    if (existing) {
      if (!existing.visible) {
        setImages((prev) =>
          prev.map((img) =>
            img.endpoint === endpoint ? { ...img, visible: true } : img,
          ),
        );
        toast("Kaavio palautettu näkyviin");
      } else {
        toast("Kaavio on jo ladattu");
      }
      return;
    }

    setLoading(true);

    try {
      const res = await apiFetch(endpoint);
      const blob = await res.blob();
     

      const imageObject = {
        url: URL.createObjectURL(blob),
        endpoint,
        visible: true,
      };
      setImages((prevImages) => [...prevImages, imageObject]);

      
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
    <div className="p-4">
      <h1 className="mb-4 text-4xl font-semibold">
        {loading ? "Kaaviot (Ladataan Kaaviota...)" : "Kaaviot"}
      </h1>

      <div className="mb-6 grid grid-cols-2 gap-3 sm:grid-cols-3 md:grid-cols-4">
        {endpoints.map((endpoint) => (
          <button
            key={endpoint[0]}
            onClick={() => LoadImage(endpoint[0])}
            className="rounded-md bg-blue-500 px-3 py-1.5 text-sm text-white shadow-sm transition hover:bg-blue-600"
          >
            {endpoint[1]}
          </button>
        ))}
      </div>

      <div className="flex flex-col gap-4">
        {images
          .filter((img) => img.visible)
          .map((img) => (
            <div
              key={img.endpoint}
              className="relative"
            >
              <img
                src={img.url}
                alt={`Image from ${img.endpoint}`}
                className="max-w-full rounded-md shadow-md"
              />
              <button
                onClick={() =>
                  setImages((prev) =>
                    prev.map((i) =>
                      i.endpoint === img.endpoint
                        ? { ...i, visible: false }
                        : i,
                    ),
                  )
                }
                className="absolute top-2 right-2 rounded bg-red-500 px-2 py-1 text-sm text-white hover:bg-red-600"
              >
                X
              </button>
            </div>
          ))}
      </div>
    </div>
  );
}
