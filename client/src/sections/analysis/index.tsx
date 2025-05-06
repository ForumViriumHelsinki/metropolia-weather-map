"use client";

import {
  getTagGraphService,
  TagGraphParams,
} from "@/app/services/tags/getTagGraphService";
import { GraphTypes, Locations } from "@/types";
import { apiFetch } from "@/utils/apiFetch";
import { capitalize } from "@/utils/capitalize";
import Image from "next/image";
import Link from "next/link";
import { useEffect, useState } from "react";
import { Tag } from "../../app/(routes)/tags/page";

const graphs = [
  { display: "Pylväs", value: "bar" },
  { display: "Viiva", value: "plot" },
];
const timesOfDay = [
  { display: "Koko päivä", value: "whole day" },
  { display: "Päiväsaika", value: "daytime" },
  { display: "Yöaika", value: "nighttime" },
];
const Analysis = () => {
  const [tags, setTags] = useState<Tag[]>([]);
  const [message, setMessage] = useState<string>("");
  const [graphUrl, setGraphUrl] = useState<string | null>(null);
  const [graphParams, setGraphParams] = useState<TagGraphParams>({
    tag1: "",
    tag2: "",
    graph_type: GraphTypes.plot,
    timeOfDay: timesOfDay[0].value,
  });
  const [imageLoaded, setImageLoaded] = useState<boolean>(false); // New state for image loading

  useEffect(() => {
    const fetchTags = async () => {
      const res = await apiFetch("/tags");
      const tags: Tag[] = await res.json();
      setTags(tags);
      setGraphParams({ ...graphParams, tag1: tags[0].id, tag2: tags[0].id });
    };
    fetchTags();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const getGraph = async () => {
    console.log("getGraph()");

    try {
      setMessage("Numeroita pyöritetään");
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
      <div className="mb-2 flex justify-between">
        <h2 className="text-4xl font-semibold">Analysointityökalu tägeille</h2>
        <Link
          href={"/tags"}
          className="text-4xl font-semibold"
        >
          Hallitse tägejä
        </Link>
      </div>
      <div className="flex flex-col-reverse gap-4 sm:grid sm:grid-cols-4 sm:grid-rows-6">
        <button
          className="btn-primary row-start-6 row-end-6"
          onClick={getGraph}
        >
          Luo kaavio
        </button>

        <form className="box-basic col-span-3 row-span-6 flex flex-col">
          <label>Tägi 1</label>
          <select
            onChange={(e) =>
              setGraphParams({ ...graphParams, tag1: e.currentTarget.value })
            }
          >
            {tags.map((t) => (
              <option
                key={t.id}
                value={t.id}
              >
                {capitalize(t.id)}
              </option>
            ))}
          </select>

          <label>Tägi 2</label>
          <select
            onChange={(e) =>
              setGraphParams({ ...graphParams, tag2: e.currentTarget.value })
            }
          >
            {tags.map((t) => (
              <option
                key={t.id}
                value={t.id}
              >
                {capitalize(t.id)}
              </option>
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
            {graphs.map((g) => (
              <option
                key={g.value}
                value={g.value}
              >
                {g.display}
              </option>
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

          <label>Vuorokaudenaika</label>
          <select
            onChange={(e) =>
              setGraphParams({
                ...graphParams,
                timeOfDay: e.currentTarget.value,
              })
            }
          >
            {timesOfDay.map((t) => (
              <option
                key={t.value}
                value={t.value}
              >
                {t.display}
              </option>
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
