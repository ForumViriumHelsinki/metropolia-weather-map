"use client";

import { createTagService } from "@/app/services/tags/createTagService";
import { addTagService } from "@/services/tags/addTagsService";
import { Sensor } from "@/types";
import { useMessageDisplay } from "@/utils/useMessageDisplay";
import React, { useState } from "react";
import { Tag } from "./page";

const TagAdding = ({
  tags,
  setTags,
  selectedSensors,
  setSelectedSensors,
}: {
  tags: Tag[];
  setTags: React.Dispatch<React.SetStateAction<Tag[]>>;
  selectedSensors: Sensor[];
  setSelectedSensors: React.Dispatch<React.SetStateAction<Sensor[]>>;
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
    try {
      await addTagService(selectedSensors, selectedTag);
      setMessage("Tags added succesfully");
      setSelectedSensors([]);
    } catch (error) {
      if (error instanceof Error) {
        setMessage(error.message);
      }
      console.error(error);
    }
  };

  return (
    <div className="box-basic grid grid-cols-2">
      <div>
        <h2 className="text-2xl">Lisää tägi</h2>
        <div className="flex flex-col gap-6">
          <div className="flex flex-col gap-2">
            <label className="text-xl font-bold">Lisättävä tägi</label>
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
              Lisää tägi sensoriin
            </button>
          </div>

          {/* Add tag to db */}
          <div>
            <form onSubmit={handleTagCreation}>
              <div className="flex flex-col gap-2">
                <label className="text-xl font-bold">Luo uusi tägi</label>
                <input
                  className="w-1/2"
                  value={newTag}
                  onChange={(e) => setNewTag(e.currentTarget.value)}
                  type="text"
                  placeholder="Luotava tägi"
                />
              </div>

              <button className="btn-primary mt-2 w-1/2">Luo tägi</button>
            </form>
            <div>{message}</div>
          </div>
        </div>
      </div>

      {/* List of selected sensors */}
      <div className="flex flex-col justify-between">
        <div>
          <h2 className="text-2xl">Valitut sensorit</h2>
          <div>
            {selectedSensors.map((s) => (
              <option key={s.id}>{s.id}</option>
            ))}
          </div>
        </div>

        <div>
          <button
            onClick={() => setSelectedSensors([])}
            className="btn-primary w-1/2"
          >
            Tyhjennä valinnat
          </button>
        </div>
      </div>
    </div>
  );
};

export default TagAdding;
