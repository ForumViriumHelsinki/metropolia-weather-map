"use client";

import { apiFetch } from "@/utils/apiFetch";
import { useState } from "react";

const Analysis = () => {
  const [graphUrl, setGraphUrl] = useState<string>("");

  const getGraph = async () => {
    const res = await apiFetch("/analysis/temperature");
    const blob = await res.blob();
    const graphUrl = URL.createObjectURL(blob);
    setGraphUrl(graphUrl);
  };

  return (
    <div>
      <h1>Analysis</h1>
      <button
        className="box-basic"
        onClick={getGraph}
      >
        Get graph
      </button>
      {graphUrl && (
        <img
          src={graphUrl}
          alt="Temperature Analysis Graph"
        />
      )}
    </div>
  );
};

export default Analysis;
