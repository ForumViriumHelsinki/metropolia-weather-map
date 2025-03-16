"use client";

import { apiFetch } from "@/utils/apiFetch";

const ClientDebug = () => {
  const handleButton = async () => {
    const res = await apiFetch("/sensors");
    console.log(await res.json());
  };

  return (
    <div className="">
      <button onClick={handleButton}>TEST</button>
    </div>
  );
};

export default ClientDebug;
