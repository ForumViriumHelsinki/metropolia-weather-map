"use client";

import { Icon } from "leaflet";
import "leaflet/dist/leaflet.css";

import { MapContainer, Marker, TileLayer } from "react-leaflet";

const sensorLocations: [number, number][] = [
  [60.19628790558516, 24.953944343215543],
  [60.19858337673502, 24.949683705063027],
  [60.19603679151048, 24.95214986305944],
];

const TestMap = () => {
  const icon = new Icon({
    iconUrl: "https://cdn-icons-png.flaticon.com/512/2776/2776000.png",
    iconSize: [38, 38],
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
      {sensorLocations.map((coords, index) => (
        <Marker
          key={index}
          position={coords}
          icon={icon}
        ></Marker>
      ))}
    </MapContainer>
  );
};

export default TestMap;
