"use client";

import { Sensor } from "@/types";
import { apiFetch } from "@/utils/apiFetch";
import dynamic from "next/dynamic";
import { useEffect, useState } from "react";
import TagAdding from "./TagAdding";

// Fixes error 500
const TagMap = dynamic(() => import("./TagMap"), { ssr: false });

export interface Tag {
  id: string;
}

const Tags = () => {
  const [tags, setTags] = useState<Tag[]>([]);
  const [selectedTag, setSelectedTag] = useState<string>("All");
  const [sensorsWithTag, setSensorsWithTag] = useState<Sensor[]>([]);
  const [selectedSensors, setSelectedSensors] = useState<Sensor[]>([]);
  const [allSensors, setAllSensors] = useState<Sensor[]>([]);

  useEffect(() => {
    const fetchAllSensors = async () => {
      const res = await apiFetch("/sensors");
      const data = await res.json();
      setAllSensors(data);
    };
    fetchAllSensors();
  }, []);

  useEffect(() => {
    const fetchTags = async () => {
      const res = await apiFetch("/tags");
      const tags: Tag[] = await res.json();
      setTags(tags);
    };
    fetchTags();
  }, []);

  useEffect(() => {
    const fetchSensors = async () => {
      const res = await apiFetch(`/sensors?tag=${selectedTag}`);
      const data = await res.json();
      setSensorsWithTag(data);
    };
    fetchSensors();
  }, [selectedTag]);

  // Add clicked sensors to list and remove if clicked again
  const handleSelectedSensors = (sensor: Sensor) => {
    if (selectedSensors.includes(sensor)) {
      setSelectedSensors((prev) => prev.filter((s) => s.id !== sensor.id));
      return;
    }

    setSelectedSensors((prev) => [...prev, sensor]);
  };

  return (
    <div className="flex flex-col gap-2">
      <TagAdding
        tags={tags}
        setTags={setTags}
        selectedSensors={selectedSensors}
        setSelectedSensors={setSelectedSensors}
      />

      <div className="box-basic">
        <div>Filter map by tag</div>
        <select onChange={(e) => setSelectedTag(e.currentTarget.value)}>
          <option>All</option>
          {tags.map((t) => (
            <option key={t.id}>{t.id}</option>
          ))}
        </select>
      </div>

      <div className="border-off-white aspect-4/2 w-full rounded-lg border">
        <TagMap
          sensors={sensorsWithTag.length === 0 ? allSensors : sensorsWithTag}
          selectedSensors={selectedSensors}
          handleSelectedSensors={handleSelectedSensors}
        />
      </div>
    </div>
  );
};

export default Tags;
