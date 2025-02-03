"use client";

import "leaflet/dist/leaflet.css";

import { MapContainer, TileLayer } from "react-leaflet";

const TestMap = () => {
  return (
    <MapContainer
      center={[60.192193, 24.961126]}
      zoom={17}
      scrollWheelZoom={true}
    >
      <TileLayer
        url="http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}"
        subdomains={["mt0", "mt1", "mt2", "mt3"]}
      />
    </MapContainer>
  );
};

export default TestMap;
