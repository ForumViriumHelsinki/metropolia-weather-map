"use client";

import { apiFetch } from "@/utils/apiFetch";
import Image from "next/image";
import { useState } from "react";

enum AnalysisDate {
  single = "single",
  between = "between",
}

enum SensorType {
  All = "all",
  Sun = "sun",
  Shade = "shade",
}

enum AnalysisTypes {
  Humidity = "humidity",
  Temperature = "temperature",
}

interface AnalysisOption {
  name: string;
  type: AnalysisTypes;
  dates: AnalysisDate;
}

const ops: AnalysisOption[] = [
  {
    name: "Average humidity per day",
    type: AnalysisTypes.Humidity,
    dates: AnalysisDate.single,
  },
  {
    name: "Average humidity between",
    type: AnalysisTypes.Humidity,
    dates: AnalysisDate.between,
  },
  {
    name: "Average temperature per day",
    type: AnalysisTypes.Temperature,
    dates: AnalysisDate.single,
  },
  {
    name: "Average temperature between",
    type: AnalysisTypes.Temperature,
    dates: AnalysisDate.between,
  },
];

interface Settings {
  sensorType: SensorType;
  startDate: string;
  endDate: string;
  selectedSensor: SensorType | string;
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

interface ResponseSummary {
  average: string;
  max: string;
  min: string;
  std_dev: string;
}

const GraphDisplay = () => {
  // Options to show needed input fields and for creating URL for data fetching
  const [options, setOptions] = useState<AnalysisOption>(ops[0]);
  // Parameters sent to API
  // SensorType saves the used type in case user selects "All in group"
  const [settings, setSettings] = useState<Settings>({
    sensorType: SensorType.All,
    startDate: "",
    endDate: "",
    selectedSensor: SensorType.All,
  });
  const [imgUrl, setImgUrl] = useState<string | null>(null);
  const [summary, setSummary] = useState<ResponseSummary | null>(null);

  const handleOption = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const index = parseInt(e.currentTarget.value, 10);
    setOptions(ops[index]);
  };

  const handleSettings = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const value = e.currentTarget.value as SensorType;

    setSettings((prev) => ({
      ...prev,
      sensorType: value,
      selectedSensor: value,
    }));
  };

  const handleSensorChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const value = e.currentTarget.value;
    console.log(value);

    // Set the value to a group if "All in group" is selected
    if (!sensors[SensorType.All].includes(value)) {
      setSettings((prev) => ({ ...prev, selectedSensor: settings.sensorType }));
      return;
    }
    setSettings((prev) => ({ ...prev, selectedSensor: value }));
  };

  const handleDateChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const key = e.currentTarget.name;
    const val = e.currentTarget.value;

    setSettings((prev) => ({
      ...prev,
      [key]: val,
    }));
  };

  const fetchGraph = async () => {
    // Check that required params exist
    if (!settings.startDate) return;

    // Return if end date is missing on analyses
    if (options.dates === AnalysisDate.between && !settings.endDate) return;

    const params = new URLSearchParams({
      start_date: settings.startDate,
      end_date: settings.endDate,
      sensor_id: settings.selectedSensor,
    });

    // If sensorType is "all" remove "sensor_id"
    // API returns data from all sensors if "sensor_id" is empty
    // TODO: refactor API to accept "all" to get data from all sensors
    if (settings.sensorType === SensorType.All) {
      params.delete("sensor_id");
    }

    // Remove params depending on options
    if (options.dates === AnalysisDate.single) {
      params.delete("end_date");
    }

    // Currently image has to be fetched separately from data
    // because broken image is returned from normal API route
    const imageRes = await apiFetch(
      `/analysis/daily-${options.type}-graph/image?${params.toString()}`,
    );
    const image = await imageRes.blob();

    const dataRes = await apiFetch(
      `/analysis/daily-${options.type}-graph?${params.toString()}`,
    );
    const data = await dataRes.json();
    setSummary(data.summary);
    setImgUrl(URL.createObjectURL(image));
  };

  return (
    <div className="flex-col-4 2xl:grid 2xl:grid-cols-4">
      <div className="graph-display flex-col-4 h-fit w-full sm:grid sm:grid-cols-2 2xl:col-span-1 2xl:grid-cols-1 2xl:grid-rows-2">
        <div className="bg-off-white px-4 py-3">
          {/* ANALYSIS */}
          <div>
            <label>Analysis</label>
            <select onChange={(e) => handleOption(e)}>
              {ops.map((a, index) => (
                <option
                  key={a.name}
                  value={index}
                  onClick={() => console.log("hello")}
                >
                  {a.name}
                </option>
              ))}
            </select>
          </div>

          {/* DATE */}
          {/* TODO: Handle case where end date is before start date and either are past current date*/}
          <div>
            <label>Date</label>
            <input
              type="date"
              name="startDate"
              onChange={(e) => handleDateChange(e)}
              value={settings.startDate}
            />
            {options?.dates === AnalysisDate.between && (
              <input
                type="date"
                name="endDate"
                onChange={(e) => handleDateChange(e)}
                value={settings.endDate}
              />
            )}
          </div>

          {/* SENSOR TYPE */}
          <div>
            <label>Sensor type</label>
            <select
              className="capitalize"
              onChange={(e) => handleSettings(e)}
            >
              {Object.values(SensorType).map((t) => (
                <option key={t}>{t}</option>
              ))}
            </select>
          </div>

          {/* SENSORS */}
          <div>
            <label>Sensors</label>
            <select
              onChange={(e) => handleSensorChange(e)}
              value={
                sensors[SensorType.All].includes(settings.selectedSensor)
                  ? settings.selectedSensor
                  : "All in group"
              }
            >
              <option>All in group</option>
              {sensors[settings.sensorType].map((s) => (
                <option
                  key={s}
                  value={s}
                >
                  {s.slice(-4)}
                </option>
              ))}
            </select>
          </div>

          <button
            className="btn-primary mt-2"
            onClick={fetchGraph}
          >
            Fetch
          </button>
        </div>

        {/* SUMMARY */}
        {summary && (
          <div className="bg-off-white h-h-full px-4 py-3 2xl:h-fit">
            <label>Summary</label>
            <span className="font-heavy">Average: </span>
            <span>{summary.average}</span>
            <span className="font-heavy">Max: </span> <span>{summary.max}</span>
            <span className="font-heavy">Min: </span> <span>{summary.min}</span>
            <span className="font-heavy">Deviation: </span>
            <span>{summary.std_dev}</span>
          </div>
        )}
      </div>

      {/* GRAPH IMAGE */}
      <div className="relative col-span-3">
        {imgUrl && (
          <Image
            className="h-auto w-full rounded-lg"
            src={imgUrl}
            alt="Image of graph"
            width={0}
            height={0}
            sizes="100vw"
          />
        )}
      </div>
    </div>
  );
};

export default GraphDisplay;
