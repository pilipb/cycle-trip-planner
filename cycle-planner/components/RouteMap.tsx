"use client";

import { MapContainer, TileLayer, GeoJSON, useMap } from "react-leaflet";
import type { RouteGeoJSON } from "@/lib/api";
import "leaflet/dist/leaflet.css";

function FitBounds({ geojson }: { geojson: RouteGeoJSON }) {
  const map = useMap();
  const features = geojson.features;
  if (!features?.length) return null;

  const coords = features.flatMap((f) => {
    const geom = f.geometry;
    if (geom?.type === "LineString" && geom.coordinates) {
      return geom.coordinates as [number, number][];
    }
    return [];
  });
  if (coords.length < 2) return null;

  const lats = coords.map((c) => c[1]);
  const lons = coords.map((c) => c[0]);
  const bounds: [[number, number], [number, number]] = [
    [Math.min(...lats), Math.min(...lons)],
    [Math.max(...lats), Math.max(...lons)],
  ];
  map.fitBounds(bounds, { padding: [20, 20], maxZoom: 12 });
  return null;
}

export default function RouteMap({
  geojson,
  className = "h-64 w-full",
}: {
  geojson: RouteGeoJSON;
  className?: string;
}) {
  return (
    <div className={`overflow-hidden rounded-lg border border-zinc-200 dark:border-zinc-700 ${className}`}>
      <MapContainer
        center={[50, 10]}
        zoom={5}
        className="h-full w-full"
        scrollWheelZoom={false}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <GeoJSON
          data={geojson}
          style={{
            color: "#16a34a",
            weight: 4,
            opacity: 0.9,
          }}
        />
        <FitBounds geojson={geojson} />
      </MapContainer>
    </div>
  );
}
