"use client";

import { Sensor } from "@/types";
import { apiFetch } from "@/utils/apiFetch";
import { useMessageDisplay } from "@/utils/useMessageDisplay";
import dynamic from "next/dynamic";
import { useEffect, useState } from "react";
import { removeTagService } from "../services/removeTagService";
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

  const [message, setMessage] = useMessageDisplay();

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

  const handleTagRemoval = async () => {
    try {
      await removeTagService(selectedSensors, selectedTag);

      // Refetch sensors with tag to update map
      const updateRes = await apiFetch(`/sensors?tag=${selectedTag}`);
      const data = await updateRes.json();
      setSensorsWithTag(data);

      setMessage("Tag removed successfully");
    } catch (error) {
      if (error instanceof Error) {
        setMessage(`Error removig tag ${error.message}`);
      }
      console.error(error);
    }
  };

  return (
    <div className="flex flex-col gap-2">
      <TagAdding
        tags={tags}
        setTags={setTags}
        selectedSensors={selectedSensors}
        setSelectedSensors={setSelectedSensors}
      />

      <div className="box-basic grid grid-cols-2">
        <div className="flex flex-col gap-3">
          <div>
            <div>Filter map by tag</div>
            <select onChange={(e) => setSelectedTag(e.currentTarget.value)}>
              <option>All</option>
              {tags.map((t) => (
                <option key={t.id}>{t.id}</option>
              ))}
            </select>
          </div>

          <button
            className="btn-primary w-fit"
            onClick={handleTagRemoval}
          >
            Remove tag
          </button>
          <div>{message}</div>
        </div>

        <div>
          <h2 className="text-2xl">Selected sensors</h2>
          {selectedSensors.map((s) => (
            <div key={s.id}>{s.id}</div>
          ))}
        </div>
      </div>

      <div className="border-off-white aspect-4/2 w-full rounded-lg border">
        <TagMap
          sensors={selectedTag === "All" ? allSensors : sensorsWithTag}
          selectedSensors={selectedSensors}
          handleSelectedSensors={handleSelectedSensors}
        />
      </div>
    </div>
  );
};

export default Tags;
