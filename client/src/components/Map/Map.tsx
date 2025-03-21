"use client";

import { Sensor } from "@/types";
import { apiFetch } from "@/utils/apiFetch";
import { Icon } from "leaflet";
import "leaflet/dist/leaflet.css";
import { useEffect, useState } from "react";
import { MapContainer, Marker, Popup, TileLayer } from "react-leaflet";

const Map = () => {
  const [sensors, setSensors] = useState<Sensor[]>([]);

  useEffect(() => {
    const getSensors = async () => {
      const res = await apiFetch("/sensors");

      if (res.status === 200) {
        const data = await res.json();
        setSensors(data);
      }
    };
    getSensors();
  }, []);

  const iconSun = new Icon({
    iconUrl: "icon_makelankatu.png",
    iconSize: [38, 38],
  });

  return (
    <MapContainer
      center={[60.19691015749769, 24.952021110782997]}
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
            position={[sensor.coordinates[1], sensor.coordinates[0]]}
            icon={iconSun}
          >
            <Popup>
              <div className="text-center text-sm font-semibold [&>span]:block">
                <span>{sensor.id.slice(-4)}</span>
              </div>
            </Popup>
          </Marker>
        ))}
    </MapContainer>
  );
};

export default Map;
