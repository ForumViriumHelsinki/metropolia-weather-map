"use client";

import { Sensor } from "@/types";
import { useState } from "react";

interface Tag {
  id: string;
}

const TagAdding = () => {
  const [tags, setTags] = useState<Tag[]>([]);
  const [selectedSensors, setSelectedSensors] = useState<Sensor[]>([]);
  const [selectedTag, setSelectedTag] = useState<string>("All");

  return (
    <div className="bg-off-white grid grid-cols-2">
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
      {/* Tag input */}
      <div>
        <div className="flex flex-col">
          <label>New tag</label>
          <input
            type="text"
            placeholder="New tag"
          />
        </div>
      </div>

      {/* List of selected sensors */}
      <div className="h-56 overflow-y-scroll">
        <select size={11}>
          {selectedSensors.map((s) => (
            <option key={s.id}>{s.id}</option>
          ))}
        </select>
      </div>
    </div>
  );
};

export default TagAdding;
