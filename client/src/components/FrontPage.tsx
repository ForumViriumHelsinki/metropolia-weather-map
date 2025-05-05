'use client';

import DropMenu from '@/components/DropMenu';
import MapWrapper from '@/components/Map/MapWrapper';
import SensorCard from '@/components/SensorCard/SensorCard';
import VallilaCard from '@/components/SensorCard/VallilaCard';
import {Sensor} from "@/types";
import { VallilaLatestData } from '@/app/page';

interface ClientHomeProps {
    vallila: Sensor[];
    koivukyla: Sensor[];
    laajasalo: Sensor[];
    latestData: VallilaLatestData[];
}

export default function ClientHome({ vallila, koivukyla, laajasalo, latestData }: ClientHomeProps) {
    return (
        <div>
            {/* Map */}
            <div className="2xl:flex 2xl:gap-12">
                <h2 className="mb-2 text-5xl 2xl:pt-9">Mäkelänkatu</h2>
                <div className="2xl:w-fill aspect-2/3 w-full border-2 sm:aspect-2/1 2xl:aspect-2/1">
                    <MapWrapper />
                </div>
            </div>

            {/* Sensor Cards */}
            {latestData.length === 0 && (
                <div className="text-xl text-red-800">
                    Error fetching latest data from server
                </div>
            )}

            <DropMenu title="Vallila">
                {vallila.map((sensor) => (
                    <VallilaCard
                        key={sensor.id}
                        sensor={sensor}
                        latestData={latestData.find((d) => d.id === sensor.id)}
                    />
                ))}
            </DropMenu>

            <DropMenu title="Koivukylä">
                {koivukyla.map((sensor) => (
                    <SensorCard
                        key={sensor.id}
                        sensor={sensor}
                        markerColor="var(--color-shade)"
                    />
                ))}
            </DropMenu>

            <DropMenu title="Laajasalo">
                {laajasalo.map((sensor) => (
                    <SensorCard
                        key={sensor.id}
                        sensor={sensor}
                        markerColor="var(--color-sun)"
                    />
                ))}
            </DropMenu>
        </div>
    );
}
