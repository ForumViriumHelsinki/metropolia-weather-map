"use client";

import { Sensor } from "@/types";
import { apiFetch } from "@/utils/apiFetch";
import { useMessageDisplay } from "@/utils/useMessageDisplay";
import React, { useState } from "react";
import { createTagService } from "../services/createTagService";
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
  const [message, setMessage] = useMessageDisplay();

  const handleTagCreation = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (!newTag) return;

    try {
      await createTagService(newTag);
      setTags((prev) => [...prev, { id: newTag }]);
      setMessage("Tag created successfully");
      setNewTag("");
    } catch (error) {
      if (error instanceof Error) {
        setMessage(error.message);
      }
      console.error(error);
    }
  };

  const handleTagAdding = async () => {
    console.log(selectedSensors);
    console.log(selectedTag);

    const body = JSON.stringify({
      ids: selectedSensors.map((s) => s.id),
      tag: selectedTag,
    });

    console.log(body);
    const res = await apiFetch("/sensor-tags", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body,
    });

    const data = await res.json();
    console.log(data);
  };

  return (
    <div className="box-basic grid grid-cols-2">
      <div>
        <h2 className="text-2xl">Add tag to sensors</h2>
        <div className="flex flex-col gap-6">
          <div className="flex flex-col">
            <label className="text-xl font-bold">Select tag to add</label>
            <select
              className="w-1/2"
              value={selectedTag}
              onChange={(e) => setSelectedTag(e.target.value)}
            >
              <option>All</option>
              {tags.map((t) => (
                <option key={t.id}>{t.id}</option>
              ))}
            </select>

            <button
              className="btn-primary w-1/2"
              onClick={handleTagAdding}
            >
              Add tag to sensors
            </button>
          </div>

          {/* Add tag to db */}
          <div>
            <form onSubmit={handleTagCreation}>
              <div className="flex flex-col">
                <label className="text-xl font-bold">Create new tag</label>
                <input
                  value={newTag}
                  onChange={(e) => setNewTag(e.currentTarget.value)}
                  type="text"
                  placeholder="New tag"
                />
              </div>

              <button className="btn-primary w-1/2">Add new tag</button>
            </form>
            <div>{message}</div>
          </div>
        </div>
      </div>

      {/* List of selected sensors */}
      <div>
        <h2 className="text-2xl">Selected sensors</h2>
        <div>
          {selectedSensors.map((s) => (
            <option key={s.id}>{s.id}</option>
          ))}
        </div>
      </div>
    </div>
  );
};

export default TagAdding;
