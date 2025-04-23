"use client";

import { Sensor } from "@/types";
import { apiFetch } from "@/utils/apiFetch";
import React, { useState } from "react";
import { Tag } from "./page";

const TagAdding = ({
  tags,
  setTags,
  selectedSensors,
}: {
  tags: Tag[];
  setTags: React.Dispatch<React.SetStateAction<Tag[]>>;
  selectedSensors: Sensor[];
}) => {
  const [selectedTag, setSelectedTag] = useState<string>("All");
  const [newTag, setNewTag] = useState<string>("");

  const handleNewTag = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (!newTag) return;

    console.log(JSON.stringify({ tag: newTag }));
    const res = await apiFetch("/tags", {
      method: "POST",
      body: JSON.stringify({ tag: newTag }),
      headers: { "Content-Type": "application/json" }, // Ensure proper headers
    });
    if (res.ok) {
      setTags((prev) => [...prev, { id: newTag }]);
    }

    setNewTag("");
  };

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

      {/* Add tag to db */}
      <div>
        <form
          className="flex flex-col"
          onSubmit={handleNewTag}
        >
          <label>New tag</label>
          <input
            value={newTag}
            onChange={(e) => setNewTag(e.currentTarget.value)}
            type="text"
            placeholder="New tag"
          />
          <button className="btn-primary">Add new tag</button>
        </form>
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
