"use client";

import { apiFetch } from "@/utils/apiFetch";
import { useEffect, useState } from "react";

interface Tag {
  id: string;
}

const Home = () => {
  const [tags, setTags] = useState<Tag[]>([]);

  useEffect(() => {
    const fetchTags = async () => {
      const res = await apiFetch("/tags");
      const tags: Tag[] = await res.json();
      setTags(tags);
    };
    fetchTags();
  }, []);

  console.log(tags);

  return (
    <div>
      <h1>Tag analysis</h1>
      <div className="bg-off-white">
        <h2>Tags</h2>
        <div>
          {tags.map((t) => (
            <div key={t.id}>{t.id}</div>
          ))}
        </div>

        <div className="flex flex-col">
          <label>New tag</label>
          <input
            type="text"
            placeholder="New tag"
          />
        </div>
      </div>
    </div>
  );
};

export default Home;
