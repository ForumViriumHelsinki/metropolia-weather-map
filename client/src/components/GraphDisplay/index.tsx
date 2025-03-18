"use client";

import { apiFetch } from "@/utils/apiFetch";
import Image from "next/image";
import { useState } from "react";

enum AnalysisDate {
  single = "single",
  between = "between",
}

enum SensorType {
  All = "All",
  Sun = "Sun",
  Shade = "Shade",
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
  const [selectedSensor, setSelectedSensor] = useState<SensorType | string>(
    SensorType.All,
  );
  const [options, setOptions] = useState<AnalysisOption>(ops[0]);
  const [settings, setSettings] = useState<Settings>({
    sensorType: SensorType.All,
    startDate: "",
    endDate: "",
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
      listedSensors: sensors[value],
    }));

    setSelectedSensor(value);
  };

  const handleSensorChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const value = e.currentTarget.value;
    console.log(value);

    if (!sensors[SensorType.All].includes(value)) {
      setSelectedSensor(settings.sensorType);
      return;
    }

    setSelectedSensor(value);
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
    if (!settings.startDate) return;
    if (options.dates === AnalysisDate.between && !settings.endDate) return;

    const params = new URLSearchParams({
      start_date: settings.startDate,
      end_date: settings.endDate,
      sensor_id: settings.sensorType,
    });

    if (settings.sensorType === SensorType.All) {
      params.delete("sensor_id");
    }

    if (options.dates === AnalysisDate.single) {
      params.delete("end_date");
    }

    console.log(options);
    console.log(`/analysis/daily-${options.type}-graph?${params.toString()}`);

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
    <div className="grid-scaling">
      <div className="graph-display col-span-1 flex h-fit grid-rows-2 flex-col gap-4">
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

          <div>
            <label>Sensor type</label>
            <select onChange={(e) => handleSettings(e)}>
              {Object.values(SensorType).map((t) => (
                <option key={t}>{t}</option>
              ))}
            </select>
          </div>

          <div>
            <label>Sensors</label>
            <select
              onChange={(e) => handleSensorChange(e)}
              value={
                sensors[SensorType.All].includes(selectedSensor)
                  ? selectedSensor
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
            className="btn-primary"
            onClick={fetchGraph}
          >
            Fetch
          </button>
        </div>
        {/* SUMMARY */}
        {summary && (
          <div className="bg-off-white px-4 py-3">
            <label>Summary</label>
            <span>Average: {summary.average}</span>
            <span>Max: {summary.max}</span>
            <span>Min: {summary.min}</span>
            <span>Deviation: {summary.std_dev}</span>
          </div>
        )}
      </div>
      <div className="relative col-span-3">
        {imgUrl && (
          <Image
            src={imgUrl}
            alt="Image of graph"
            width={0}
            height={0}
            sizes="100vw"
            style={{ width: "100%", height: "auto" }} // optional
          />
        )}
      </div>
    </div>
  );
};

export default GraphDisplay;
