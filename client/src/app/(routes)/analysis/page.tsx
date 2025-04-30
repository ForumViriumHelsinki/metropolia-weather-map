"use client";

import {
  getTagGraphService,
  TagGraphParams,
} from "@/app/services/tags/getTagGraphService";
import { GraphTypes, Locations } from "@/types";
import { useState } from "react";

const Analysis = () => {
  const [message, setMessage] = useState<string>("");
  const [graphUrl, setGraphUrl] = useState<string | null>(null);
  const [graphParams, setGraphParams] = useState<TagGraphParams>({
    tag1: "",
    tag2: "",
    graph_type: GraphTypes.plot,
  });

  const getGraph = async () => {
    console.log("getGraph()");

    try {
      setGraphUrl(null);
      setMessage("Crunching numbers");
      const blob = await getTagGraphService(graphParams);
      setGraphUrl(URL.createObjectURL(blob));
    } catch (error) {
      if (error instanceof Error) {
        setMessage(`Error creating graph: ${error.message}`);
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
        <select
          onChange={(e) =>
            setGraphParams({
              ...graphParams,
              location: e.currentTarget.value as Locations,
            })
          }
        >
          <option value={""}>All</option>
          {Object.values(Locations).map((loc) => (
            <option
              key={loc}
              value={loc}
            >
              {loc}
            </option>
          ))}
        </select>

        <label>Start date</label>
        <input
          type="date"
          onChange={(e) =>
            setGraphParams({
              ...graphParams,
              start_date: e.currentTarget.value,
            })
          }
        />

        <label>End date</label>
        <input
          type="date"
          onChange={(e) =>
            setGraphParams({
              ...graphParams,
              end_date: e.currentTarget.value,
            })
          }
        />

        <label>Graph type</label>
        <select
          onChange={(e) =>
            setGraphParams({
              ...graphParams,
              graph_type: e.currentTarget.value as GraphTypes,
            })
          }
        >
          {Object.values(GraphTypes).map((gt) => (
            <option
              key={gt}
              // value={gt}
            >
              {gt}
            </option>
          ))}
        </select>
      </form>
      {graphUrl ? (
        // eslint-disable-next-line @next/next/no-img-element
        <img
          src={graphUrl}
          alt="Temperature Analysis Graph"
          onLoad={() => {
            console.log("hello");
            setMessage("");
          }}
        />
      ) : (
        <div>{message}</div>
      )}
    </div>
  );
};

export default Analysis;
