"use client";

import { getSensorsService } from "@/app/services/getSensorsService";
import { Sensor } from "@/types";
import { Icon } from "leaflet";
import "leaflet/dist/leaflet.css";
import { useEffect, useState } from "react";

import { MapContainer, Marker, Popup, TileLayer } from "react-leaflet";

const TestMap = () => {
  const [sensors, setSensors] = useState<Sensor[]>([]);

  useEffect(() => {
    const getSensors = async () => {
      setSensors(await getSensorsService());
    };
    getSensors();
  }, []);
  console.log("hello", sensors);

  const iconSun = new Icon({
    iconUrl: "icon_sun.png",
    iconSize: [38, 38],
  });

  const iconShade = new Icon({
    iconUrl: "icon_shade.png",
    iconSize: [40, 40],
  });

  return (
    <MapContainer
      center={[60.19628790558516, 24.953944343215543]}
      zoom={16}
      scrollWheelZoom={true}
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      {sensors &&
        sensors.map((sensor) => (
          <Marker
            key={sensor.id}
            position={[sensor.location[1], sensor.location[0]]}
            icon={sensor.type === "Auringossa" ? iconSun : iconShade}
          >
            <Popup>
              <div className="text-center text-sm font-semibold [&>span]:block">
                <span>{sensor.id.slice(-4)}</span>
                <span>{sensor.note}</span>
              </div>
            </Popup>
          </Marker>
        ))}
    </MapContainer>
  );
};

export default TestMap;
