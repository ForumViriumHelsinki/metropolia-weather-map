"use client";

import { apiFetch } from "@/utils/apiFetch";
import Image from "next/image";
import { useState } from "react";

enum SensorType {
  All = "all",
  Sun = "sun",
  Shade = "shade",
}

const sensors = {
  [SensorType.All]: [
    "24E124136E106616",
    "24E124136E106617",
    "24E124136E106618",
    "24E124136E106619",
    "24E124136E106635",
    "24E124136E106636",
    "24E124136E106637",
    "24E124136E106638",
    "24E124136E106643",
    "24E124136E106661",
    "24E124136E106674",
    "24E124136E106686",
  ],
  [SensorType.Sun]: [
    "24E124136E106637",
    "24E124136E106638",
    "24E124136E106619",
    "24E124136E106661",
  ],
  [SensorType.Shade]: [
    "24E124136E106616",
    "24E124136E106617",
    "24E124136E106618",
    "24E124136E106635",
    "24E124136E106636",
    "24E124136E106643",
    "24E124136E106674",
    "24E124136E106686",
  ],
};

interface Options {
  dateOptions: "single" | "range" | "none";
  listedSensors: string[];
}

interface GraphParameters {
  analysisType: "unselected" | "humidity" | "temperature";
  sensorType: "all" | "sun" | "shade";

  startDate?: string;
  endDate?: string;
  sensors?: SensorType;

  sensorId?: string;
}

// Works by leveraging the holy spirit and prayers
// Will get refactored later

const GraphDisplay = () => {
  const [options, setOptions] = useState<Options>({
    dateOptions: "none",
    listedSensors: sensors[SensorType.All],
  });
  const [params, setParams] = useState<GraphParameters>({
    sensorType: "all",
    sensorId: "all",
    analysisType: "unselected",
  });

  const [imgUrl, setImgUrl] = useState<string | null>(null);

  const handleOptionChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const key = e.currentTarget.name;
    const value = e.currentTarget.value;

    if (key === "sensorType") {
      const newSensors = sensors[value as SensorType];
      setOptions((prev) => ({ ...prev, listedSensors: newSensors }));
      setParams((prev) => ({ ...prev, sensorId: value }));
      return;
    }

    if (key === "dateOptions") {
      setOptions((prev) => ({
        ...prev,
        dateOptions: value as "single" | "range" | "none",
      }));
    }

    setOptions((prev) => ({ ...prev, [key]: value }));
  };

  const handleDateChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const key = e.currentTarget.name;
    const value = e.currentTarget.value;

    setParams((prev) => ({
      ...prev,
      [key]: value,
    }));
  };

  const fetchGraph = async () => {
    console.log("fetch graph");
    console.log(params.startDate);
    if (params.analysisType === "unselected") return;
    if (!params.startDate) return;

    const urlParams = new URLSearchParams({
      start_date: params.startDate,
    });

    if (params.endDate) {
      urlParams.append("end_date", params.endDate);
    }

    if (params.sensorId) {
      urlParams.append("sensor_id", params.sensorId);
    }

    console.log(urlParams.toString());
    const res = await apiFetch(
      `/analysis/daily-${params.analysisType}-graph?${urlParams}`,
    );
    const data = await res.blob();
    const graphUrl = URL.createObjectURL(data);
    setImgUrl(graphUrl);
  };

  const handleGraphOptions = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const key = e.currentTarget.name;
    const value = e.currentTarget.value;

    if (key === "sensorId" && value === "all") {
      setParams((prev) => ({
        ...prev,
        sensorId: params.sensorType,
      }));
      return;
    }

    setParams((prev) => ({
      ...prev,
      [key]: value,
    }));
  };

  return (
    <div className="flex flex-col gap-4">
      <div className="flex">
        {/* ----- QUERY OPTIONS ----- */}
        <div className="graph-selection bg-off-white flex min-h-[370px] min-w-[200px] flex-col gap-2 rounded-l-xl px-4 py-3">
          {/* ------ ANALYSIS METRIC ------ */}
          <div>
            <label>Analysis type</label>
            <select
              name="analysisType"
              onChange={(e) => handleGraphOptions(e)}
            >
              <option value="unselected">Select</option>
              <option value="humidity">Humidity</option>
              <option value="temperature">Temperature</option>
            </select>
          </div>

          {/* ------ DATE RANGE OPTION ------ */}
          <div>
            <label>Graph range</label>
            <select
              name="dateOptions"
              onChange={(e) => handleOptionChange(e)}
            >
              <option value="none">Select</option>
              <option value="single">Single day</option>
              <option value="range">Date range</option>
            </select>
          </div>

          {/* ------ DATES ------ */}
          {options.dateOptions !== "none" && (
            <div>
              {options.dateOptions === "single" ? (
                <>
                  <label>Date</label>
                  <input
                    name="startDate"
                    type="date"
                    onChange={(e) => handleDateChange(e)}
                  />
                </>
              ) : (
                <>
                  <label>Date range</label>
                  <input
                    className="mb-1"
                    name="startDate"
                    type="date"
                    onChange={(e) => handleDateChange(e)}
                  />
                  <input
                    name="endDate"
                    type="date"
                    onChange={(e) => handleDateChange(e)}
                  />
                </>
              )}
            </div>
          )}

          {/* ------ SENSOR LOCATION ------ */}
          <div>
            <label>Sensor location</label>
            <select
              name="sensorType"
              onChange={(e) => {
                handleGraphOptions(e);
                handleOptionChange(e);
              }}
            >
              <option value={SensorType.All}>All</option>
              <option value={SensorType.Sun}>Sun</option>
              <option value={SensorType.Shade}>Shade</option>
            </select>
          </div>

          {/* ------ SENSOR ID ------ */}
          <div>
            <label>Sensor Id</label>
            <select
              name="sensorId"
              onChange={(e) => handleGraphOptions(e)}
            >
              <option value="all">All in group</option>
              {options.listedSensors.map((s) => (
                <option
                  key={s}
                  value={s}
                >
                  {s.slice(-4)}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* ----- IMAGE ----- */}
        <div className="relative aspect-10/5 grow-1 border-2">
          {imgUrl && (
            <Image
              src={imgUrl}
              fill
              alt="Graph displaying data"
            />
          )}
        </div>
      </div>

      <button
        className="btn-primary w-fit"
        onClick={fetchGraph}
      >
        Test Fetch
      </button>
    </div>
  );
};

export default GraphDisplay;
