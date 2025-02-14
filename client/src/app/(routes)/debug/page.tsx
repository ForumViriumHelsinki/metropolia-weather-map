"use client";

import { apiFetch } from "@/app/api/lib/apiFetch";

const Debug = () => {
  const test = async () => {
    const res = await apiFetch("/test");
    console.log(await res.json());
  };

  return (
    <div>
      <button onClick={test}>TEST</button>
    </div>
  );
};

export default Debug;
