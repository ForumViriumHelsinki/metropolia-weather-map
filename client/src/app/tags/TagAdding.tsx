"use client";

import { Sensor } from "@/types";
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

  const handleNewTag = async (e: React.FormEvent<HTMLFormElement>) => {
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
        <div>{message}</div>
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
