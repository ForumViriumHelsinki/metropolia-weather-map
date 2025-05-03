"use client";
import { useState } from "react";
import { apiFetch } from "@/utils/apiFetch";
import toast from 'react-hot-toast';

export default function GraphsLoader() {
    const [images, setImages] = useState([]);
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
        ["/plot/temp_vs_humidity_correlation", "Lämpötilan ja kosteuden korrelaatio"],
        ["/plot/daily_temperature_range", "Päivittäinen lämpötilaero"],
        ["/plot/daily_median_temperature", "Päivittäinen keskilämpötila"],
        ["/plot/monthly_night_temperature", "Kuukausittainen yö lämpötila"],
        ["/plot/monthly_night_min_temperature", "Kuukausittainen minimilämpötila"],
        ["/plot/monthly_night_temperature_difference", "Kuukausittainen yö lämpötilaero"],
        ["/plot/daily_median_humidity", "Päivittäinen keski kosteus"],
        ["/plot/daily_humidity_range", "Päivittäinen kosteus ero"],
        ["/plot/day_night_humidity_difference", "Päivä-yö kosteus ero"],
        ["/plot/monthly_night_humidity", "Kuukausittainen yö kosteus"],
    ];

    const LoadAllImages = async () => {
        setLoading(true);


        try {
            const endpointsToFetch = endpoints.filter(
                (endpoint) => !fetchedEndpoints.has(endpoint),
            );
            const fetches = endpointsToFetch.map((endpoint) =>
                apiFetch(endpoint[0]).then((res) => res.blob()),
            );
            const blobs = await Promise.all(fetches);

            const imageObjectUrls = blobs.map((blob) => URL.createObjectURL(blob));

            setImages((prevImages) => [...prevImages, ...imageObjectUrls]);
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

    const LoadImage = async (endpoint) => {
        if (fetchedEndpoints.has(endpoint)) {
            console.log(`Already fetched: ${endpoint}`);
            toast("Kaavio on jo ladattu");
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
        <div className="p-4">
            <h1 className="mb-4 text-4xl font-semibold">{loading ? "Kaaviot (Ladataan Kaaviota...)" : "Kaaviot"}</h1>

            <div className="mb-6 grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3">
                <button
                    onClick={LoadAllImages}
                    className="rounded-md bg-blue-500 px-3 py-1.5 text-sm text-white shadow-sm hover:bg-blue-600 transition"
                >
                    Lataa kaikkia kaaviot (Hidas)
                </button>
                {endpoints.map((endpoint) => (
                    <button
                        key={endpoint[0]}
                        onClick={() => LoadImage(endpoint[0])}
                        className="rounded-md bg-blue-500 px-3 py-1.5 text-sm text-white shadow-sm hover:bg-blue-600 transition"
                    >
                        {endpoint[1]}
                    </button>
                ))}
            </div>

            <div className="flex flex-col gap-4">
                {images.map((imgSrc, index) => (
                    <img
                        key={index}
                        src={imgSrc}
                        alt={`Image ${index}`}
                        className="max-w-full rounded-md shadow-md"
                    />
                ))}
            </div>
        </div>
    );

}
