"use client";

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

interface AnalysisOption {
  name: string;
  dates: AnalysisDate;
}

const ops: AnalysisOption[] = [
  { name: "Average humidity per day", dates: AnalysisDate.single },
  { name: "Average humidity between", dates: AnalysisDate.between },
  { name: "Average temperature per day", dates: AnalysisDate.single },
  { name: "Average temperature between", dates: AnalysisDate.between },
];

interface Settings {
  sensorType: SensorType;
  listedSensors: string[];
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

const GraphDisplay = () => {
  const [selectedSensor, setSelectedSensor] = useState<SensorType | string>(
    SensorType.All,
  );
  const [option, setOption] = useState<AnalysisOption>();
  const [settings, setSettings] = useState<Settings>({
    sensorType: SensorType.All,
    listedSensors: sensors[SensorType.All],
  });

  const handleOption = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const index = parseInt(e.currentTarget.value, 10);
    setOption(ops[index]);
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

  return (
    <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4">
      <div className="graph-display col-span-1 flex w-full flex-col bg-red-400">
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
          {option?.dates === AnalysisDate.single ? (
            <input type="date" />
          ) : (
            <>
              <input type="date" />
              <input type="date" />
            </>
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
      </div>
      <div className="col-span-3 w-full bg-amber-300">Graph</div>
    </div>
  );
};

export default GraphDisplay;
