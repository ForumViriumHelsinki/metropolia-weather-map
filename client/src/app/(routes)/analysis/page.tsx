"use client";

import {
  getTagGraphService,
  TagGraphParams,
} from "@/app/services/tags/getTagGraphService";
import { useMessageDisplay } from "@/utils/useMessageDisplay";
import { useState } from "react";

const Analysis = () => {
  const [graphUrl, setGraphUrl] = useState<string>("");
  const [graphParams, setGraphParams] = useState<TagGraphParams>({
    tag1: "",
    tag2: "",
    graph_type: "plot",
  });

  const [loadingMessage, setLoadingMessage] = useMessageDisplay();

  const getGraph = async () => {
    console.log("getGraph()");

    try {
      setLoadingMessage("Crunching numbers");
      const blob = await getTagGraphService(graphParams);
      setGraphUrl(URL.createObjectURL(blob));
      setLoadingMessage("");
    } catch (error) {
      if (error instanceof Error) {
        setLoadingMessage(`Error creating graph: ${error.message}`);
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

      {loadingMessage && (
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
