"use client";

import {
  getTagGraphService,
  TagGraphParams,
} from "@/app/services/tags/getTagGraphService";
import { GraphTypes, Locations } from "@/types";
import { apiFetch } from "@/utils/apiFetch";
import Image from "next/image";
import { useEffect, useState } from "react";
import { Tag } from "../tags/page";

const Analysis = () => {
  const [tags, setTags] = useState<Tag[]>([]);
  const [message, setMessage] = useState<string>("");
  const [graphUrl, setGraphUrl] = useState<string | null>(null);
  const [graphParams, setGraphParams] = useState<TagGraphParams>({
    tag1: "",
    tag2: "",
    graph_type: GraphTypes.plot,
  });
  const [imageLoaded, setImageLoaded] = useState<boolean>(false); // New state for image loading

  useEffect(() => {
    const fetchTags = async () => {
      const res = await apiFetch("/tags");
      const tags: Tag[] = await res.json();
      setTags(tags);
    };
    fetchTags();
  }, []);

  const getGraph = async () => {
    console.log("getGraph()");

    try {
      // setGraphUrl(null);
      setMessage("Crunching numbers");
      const blob = await getTagGraphService(graphParams);
      setGraphUrl(URL.createObjectURL(blob));
      setMessage("Graph created");
    } catch (error) {
      if (error instanceof Error) {
        setMessage(`Error creating graph: ${error.message}`);
        console.error(error);
      }
    }
  };

  return (
    <div>
      <div className="flex flex-col-reverse gap-4 sm:grid sm:grid-cols-4 sm:grid-rows-6">
        <button
          className="btn-primary row-start-6 row-end-6"
          onClick={getGraph}
        >
          Luo kaavio
        </button>

        <form className="box-basic col-span-3 row-span-6 flex flex-col">
          <label>Tag 1</label>
          <select
            onChange={(e) =>
              setGraphParams({ ...graphParams, tag1: e.currentTarget.value })
            }
          >
            {tags.map((t) => (
              <option key={t.id}>{t.id}</option>
            ))}
          </select>

          <label>Tag 2</label>
          <select
            onChange={(e) =>
              setGraphParams({ ...graphParams, tag2: e.currentTarget.value })
            }
          >
            {tags.map((t) => (
              <option key={t.id}>{t.id}</option>
            ))}
          </select>

          <label>Alue</label>
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
          <label>Kaaviotyyppi</label>
          <select
            onChange={(e) =>
              setGraphParams({
                ...graphParams,
                graph_type: e.currentTarget.value as GraphTypes,
              })
            }
          >
            {Object.values(GraphTypes).map((gt) => (
              <option key={gt}>{gt}</option>
            ))}
          </select>

          <label>Aloituspäivä</label>
          <input
            type={graphParams.graph_type === "plot" ? "date" : "month"}
            onChange={(e) =>
              setGraphParams({
                ...graphParams,
                startDate: e.currentTarget.value,
              })
            }
          />

          <label>Lopetuspäivä</label>
          <input
            type={graphParams.graph_type === "plot" ? "date" : "month"}
            onChange={(e) =>
              setGraphParams({
                ...graphParams,
                endDate: e.currentTarget.value,
              })
            }
          />

          <label>Päivänaika</label>
          <select
            onChange={(e) =>
              setGraphParams({
                ...graphParams,
                timeOfDay: e.currentTarget.value,
              })
            }
          >
            {["whole day", "daytime", "nighttime"].map((t) => (
              <option key={t}>{t}</option>
            ))}
          </select>
        </form>
      </div>

      <div
        className="box-basic relative my-4"
        style={{ display: !message ? "none" : "block" }}
      >
        {message && <div className="text-2xl font-bold">{message}</div>}

        {graphUrl && (
          <Image
            className={`${!imageLoaded ? "max-h-0" : "max-h-[600px]"} my-2 w-full transition-all duration-300`}
            src={graphUrl}
            alt="Analysis Graph"
            width={0}
            height={0}
            onLoadingComplete={() => setImageLoaded(true)}
          />
        )}
      </div>
    </div>
  );
};

export default Analysis;
