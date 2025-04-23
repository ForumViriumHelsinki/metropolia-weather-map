"use client";

import { Sensor } from "@/types";
import { Icon } from "leaflet";
import "leaflet/dist/leaflet.css";
import { MapContainer, Marker, Popup, TileLayer } from "react-leaflet";

const TagMap = ({
  sensors,
  handleSelectedSensors,
}: {
  sensors: Sensor[];
  handleSelectedSensors: (sensor: Sensor) => void;
}) => {
  const iconMakelankatu = new Icon({
    iconUrl: "icon_makelankatu.png",
    iconSize: [38, 38],
  });

  const iconKoivukyla = new Icon({
    iconUrl: "icon_koivukyla.png",
    iconSize: [38, 38],
  });

  const iconLaajasalo = new Icon({
    iconUrl: "icon_laajasalo.png",
    iconSize: [38, 38],
  });

  let icon = iconMakelankatu;

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
      {sensors.map((sensor) => {
        if (sensor.location === "Koivukylä") icon = iconKoivukyla;
        if (sensor.location === "Laajasalo") icon = iconLaajasalo;
        return (
          <Marker
            key={sensor.id}
            position={[sensor.lat, sensor.lon]}
            icon={icon}
            eventHandlers={{ click: () => handleSelectedSensors(sensor) }}
          >
            <Popup>
              <div className="text-center text-sm font-semibold [&>span]:block">
                <span>{sensor.id.slice(-4)}</span>
              </div>
            </Popup>
          </Marker>
        );
      })}
    </MapContainer>
  );
};

export default TagMap;
