"use client";

import {
  getTagGraphService,
  TagGraphParams,
} from "@/app/services/tags/getTagGraphService";
import { useState } from "react";

const Analysis = () => {
  const [graphUrl, setGraphUrl] = useState<string>("");
  const [graphParams, setGraphParams] = useState<TagGraphParams>({
    tag1: "",
    tag2: "",
    location: "",
    graph_type: "",
  });

  const getGraph = async () => {
    try {
      const blob = await getTagGraphService({
        tag1: "meri",
        tag2: "manner",
        location: "Vallila",
        graph_type: "plot",
      });
      setGraphUrl(URL.createObjectURL(blob));
    } catch (error) {
      if (error instanceof Error) {
        console.error(error);
      }
    }
  };

  return (
    <div className="flex flex-col gap-4">
      <h1>Analysis</h1>

      <button
        className="box-basic"
        onClick={getGraph}
      >
        Get graph
      </button>

      <form className="box-basic flex flex-col">
        <label>Tag1</label>
        <input
          type="text"
          value={graphParams.tag1}
          onChange={(e) =>
            setGraphParams({ ...graphParams, tag1: e.currentTarget.value })
          }
        />

        <label>Tag2</label>
        <input
          type="text"
          value={graphParams.tag2}
          onChange={(e) =>
            setGraphParams({ ...graphParams, tag2: e.currentTarget.value })
          }
        />

        <label>Location</label>
        <input
          type="text"
          value={graphParams.location}
          onChange={(e) =>
            setGraphParams({ ...graphParams, location: e.currentTarget.value })
          }
        />

        <label>Graph type</label>
        <input
          type="text"
          value={graphParams.graph_type}
          onChange={(e) =>
            setGraphParams({
              ...graphParams,
              graph_type: e.currentTarget.value,
            })
          }
        />
      </form>

      {graphUrl && (
        // eslint-disable-next-line @next/next/no-img-element
        <img
          src={graphUrl}
          alt="Temperature Analysis Graph"
        />
      )}
    </div>
  );
};

export default Analysis;
