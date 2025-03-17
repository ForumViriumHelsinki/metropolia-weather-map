"use client";

import { apiFetch } from "@/utils/apiFetch";
import { useState } from "react";

const sensors = {
  all: [
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
  sun: [
    "24E124136E106637",
    "24E124136E106638",
    "24E124136E106619",
    "24E124136E106661",
  ],
  shade: [
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
// Humidity per day
// start_date: yyyy-mm-dd
// end_date: yyyy-mm-dd
// sensorid: sun, shade, all, id

// Temperature per day
// start_date: yyyy-mm-dd
// end_date: yyyy-mm-dd
// sensorid: sun, shade, all, id

interface GraphOptions {
  analysisType?: "humidity" | "temperature";
  dateType?: "single" | "range";
  start_date?: string;
  sensor_type: "all" | "sun" | "shade";
  end_date?: string;
  sensorIds: string[];
  singleId?: string;
}

const GraphDisplay = () => {
  const [options, setOptions] = useState<GraphOptions>({
    sensorIds: sensors.all,
    sensor_type: "all",
  });

  const [imgUrl, setImgUrl] = useState<string | null>(null);

  const handleOptionChange = (option: React.ChangeEvent<HTMLSelectElement>) => {
    const key = option.currentTarget.name;
    const value = option.currentTarget.value;

    if (key === "sensorIds") {
      const selectedSensors = sensors[value as keyof typeof sensors]; // Get the correct sensor array
      setOptions((prevOptions) => ({
        ...prevOptions,
        sensor_type: value as "all" | "sun" | "shade",
        sensorIds: selectedSensors,
      }));
      return;
    }

    if (key === "idSelection") {
      if (!value) {
        setOptions((prevOptions) => ({
          ...prevOptions,
          singleId: value,
        }));
        return;
      }

      setOptions((prevOptions) => ({
        ...prevOptions,
        singleId: value,
      }));
      return;
    }

    setOptions((prevOptions) => ({
      ...prevOptions,
      [key]: value,
    }));
  };

  const handleDateChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const key = e.currentTarget.name;
    const value = e.currentTarget.value;

    setOptions((prevOptions) => ({
      ...prevOptions,
      [key]: value,
    }));
  };

  const testFetch = async () => {
    const urlParams = new URLSearchParams({
      start_date: options.start_date!,
      // sensor_id: options.sensor_type!,
    });
    console.log(urlParams.toString());
    const res = await apiFetch(`/analysis/daily-humidity-graph?${urlParams}`);
    const data = await res.blob();
    const graphUrl = URL.createObjectURL(data);
    setImgUrl(graphUrl);
  };

  return (
    <div className="flex bg-green-300">
      <button onClick={testFetch}>Test Fetch</button>
      <div className="flex w-1/5 flex-col">
        {/* ------ ANALYSIS METRIC ------ */}
        <label>Analysis type</label>
        <select
          name="analysisType"
          onChange={(e) => handleOptionChange(e)}
        >
          <option value="unselected">Select</option>
          <option value="humidity">Humidity</option>
          <option value="temperature">Temperature</option>
        </select>

        {/* ------ DATE RANGE OPTION ------ */}
        <label>Graph range</label>
        <select
          name="dateType"
          onChange={(e) => handleOptionChange(e)}
        >
          <option value="unselected">Select</option>
          <option value="single">Single day</option>
          <option value="range">Date range</option>
        </select>

        {/* ------ DATES ------ */}
        {options.dateType && (
          <>
            {options.dateType === "single" ? (
              <>
                <label>Date</label>
                <input
                  name="start_date"
                  type="date"
                  onChange={(e) => handleDateChange(e)}
                />
              </>
            ) : (
              <>
                <label>Date range</label>
                <input
                  name="start_date"
                  type="date"
                  onChange={(e) => handleDateChange(e)}
                />
                <input
                  name="end_date"
                  type="date"
                  onChange={(e) => handleDateChange(e)}
                />
              </>
            )}
          </>
        )}

        {/* ------ SENSOR LOCATION ------ */}
        <label>Sensor location</label>
        <select
          name="sensorIds"
          onChange={(e) => handleOptionChange(e)}
        >
          <option value="all">All</option>
          <option value="sun">Sun</option>
          <option value="shade">Shade</option>
        </select>

        {/* ------ SENSOR ID ------ */}
        <label>Sensor Id</label>
        <select
          name="idSelection"
          onChange={(e) => handleOptionChange(e)}
        >
          <option value="">All in group</option>
          {options.sensorIds.map((s) => (
            <option
              key={s}
              value={s}
            >
              {s.slice(-4)}
            </option>
          ))}
        </select>
      </div>

      {imgUrl && (
        <img
          src={imgUrl}
          alt="test"
        />
      )}
    </div>
  );
};

export default GraphDisplay;
