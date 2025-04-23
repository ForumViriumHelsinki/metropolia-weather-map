"use client";

import { Sensor } from "@/types";
import { apiFetch } from "@/utils/apiFetch";
import { useEffect, useState } from "react";
import TagAdding from "./TagAdding";
import TagMap from "./TagMap";

interface Tag {
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

  console.log(tags);

  return (
    <div>
      <h1>Tag analysis</h1>
      <div className="flex flex-col gap-2">
        <div className="bg-off-white grid grid-cols-2">
          {/* List of tags */}
          <div>
            <h2>Tags</h2>
            <select
              value={selectedTag}
              onChange={(e) => setSelectedTag(e.target.value)}
            >
              <option>All</option>
              {tags.map((t) => (
                <option key={t.id}>{t.id}</option>
              ))}
            </select>
          </div>

          {/* Sensors with tag */}
          <div className="h-56 overflow-y-scroll">
            {sensorsWithTag.map((s) => (
              <div
                key={s.id}
                className="grid grid-cols-2"
              >
                <div>{s.id}</div>
                <div>{s.location}</div>
              </div>
            ))}
          </div>
        </div>

        <TagAdding />

        {/* <div className="bg-off-white grid grid-cols-2">
          <div>
            <h2>Add tag to sensor</h2>
            <select
              value={selectedTag}
              onChange={(e) => setSelectedTag(e.target.value)}
            >
              <option>All</option>
              {tags.map((t) => (
                <option key={t.id}>{t.id}</option>
              ))}
            </select>
          </div>

          <div>
            <div className="flex flex-col">
              <label>New tag</label>
              <input
                type="text"
                placeholder="New tag"
              />
            </div>
          </div>

          <div className="h-56 overflow-y-scroll">
            <select size={11}>
              {selectedSensors.map((s) => (
                <option key={s.id}>{s.id}</option>
              ))}
            </select>
          </div>
        </div> */}

        <div className="aspect-4/2 w-full">
          <TagMap
            sensors={sensorsWithTag.length === 0 ? allSensors : sensorsWithTag}
            handleSelectedSensors={handleSelectedSensors}
          />
        </div>
      </div>
    </div>
  );
};

export default Tags;
