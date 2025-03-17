"use client";

import React, { useState } from "react";

const FilterDataComponent: React.FC = () => {
  const [sensorId, setSensorId] = useState<string>("");
  const [startDate, setStartDate] = useState<string>("");
  const [endDate, setEndDate] = useState<string>("");
  const [temperatureFrom, setTemperatureFrom] = useState<string>("");
  const [temperatureTo, setTemperatureTo] = useState<string>("");
  const [humidityFrom, setHumidityFrom] = useState<string>("");
  const [humidityTo, setHumidityTo] = useState<string>("");
  const [includeSensorId, setIncludeSensorId] = useState<boolean>(true);
  const [includeDateRange, setIncludeDateRange] = useState<boolean>(true);
  const [includeTemperature, setIncludeTemperature] = useState<boolean>(true);
  const [includeHumidity, setIncludeHumidity] = useState<boolean>(true);

  const handleSubmit = async () => {
    const params = new URLSearchParams();

    if (sensorId) {
      params.append("sensor_id", sensorId);
    }
    if (startDate) {
      params.append("start_date", startDate);
    }
    if (endDate) {
      params.append("end_date", endDate);
    }
    if (temperatureFrom) {
      params.append("temperature_from", temperatureFrom);
    }
    if (temperatureTo) {
      params.append("temperature_to", temperatureTo);
    }
    if (humidityFrom) {
      params.append("humidity_from", humidityFrom);
    }
    if (humidityTo) {
      params.append("humidity_to", humidityTo);
    }

    const fieldsToInclude: string[] = [];
    if (includeSensorId) {
      fieldsToInclude.push("sensor");
    }
    if (includeDateRange) {
      fieldsToInclude.push("time");
    }
    if (includeTemperature) {
      fieldsToInclude.push("temperature");
    }
    if (includeHumidity) {
      fieldsToInclude.push("humidity");
    }
    fieldsToInclude.forEach((field) => params.append("fields", field));

    const url = "http://localhost:8000/api/sensordata/?" + params.toString();

    try {
      const res = await fetch(url);
      if (!res.ok) {
        throw new Error("Failed to fetch data");
      }
      const data = await res.json();
      console.log(data);
    } catch (error) {
      console.error(error);
    }
  };

  const handleClear = () => {
    setSensorId("");
    setStartDate("");
    setEndDate("");
    setTemperatureFrom("");
    setTemperatureTo("");
    setHumidityFrom("");
    setHumidityTo("");
    setIncludeSensorId(true);
    setIncludeDateRange(true);
    setIncludeTemperature(true);
    setIncludeHumidity(true);
  };

  return (
    <div className="w-min rounded border border-gray-300 bg-offWhite p-4 shadow">
      {/* Header */}
      <div className="mb-4 bg-offWhite py-2">
        <h2 className="text-center text-lg font-semibold">Search Data</h2>
      </div>

      {/* Sensor ID (example row) */}
      <div className="mb-3 flex items-center">
        <input
          type="checkbox"
          className="mr-2"
          checked={includeSensorId}
          onChange={(e) => setIncludeSensorId(e.target.checked)}
        />
        <label className="mr-2 text-sm font-medium">Sensor</label>
        <input
          type="text"
          className="flex-grow rounded border border-gray-300 px-2 py-1 text-sm"
          placeholder="Enter value"
          value={sensorId}
          onChange={(e) => setSensorId(e.target.value)}
        />
      </div>

      {/* Date Range */}
      <div className="mb-3">
        <label className="mb-1 block text-sm font-medium">
          Date/Time Range
        </label>
        <div className="flex space-x-2">
          <input
            type="checkbox"
            className="mr-2"
            checked={includeDateRange}
            onChange={(e) => setIncludeDateRange(e.target.checked)}
          />
          <input
            type="datetime-local"
            className="w-1/2 rounded border border-gray-300 px-2 py-1 text-sm"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
          />
          <input
            type="datetime-local"
            className="w-1/2 rounded border border-gray-300 px-2 py-1 text-sm"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
          />
        </div>
      </div>

      {/* Temperature Range */}
      <div className="mb-3 flex items-center">
        <input
          type="checkbox"
          className="mr-2"
          checked={includeTemperature}
          onChange={(e) => setIncludeTemperature(e.target.checked)}
        />
        <label className="mr-2 text-sm font-medium">Temperature</label>
        <input
          type="number"
          className="mr-2 w-16 rounded border border-gray-300 px-2 py-1 text-sm"
          placeholder="From"
          value={temperatureFrom}
          onChange={(e) => setTemperatureFrom(e.target.value)}
        />
        <input
          type="number"
          className="w-16 rounded border border-gray-300 px-2 py-1 text-sm"
          placeholder="To"
          value={temperatureTo}
          onChange={(e) => setTemperatureTo(e.target.value)}
        />
      </div>

      {/* Humidity Range */}
      <div className="mb-3 flex items-center">
        <input
          type="checkbox"
          className="mr-2"
          checked={includeHumidity}
          onChange={(e) => setIncludeHumidity(e.target.checked)}
        />
        <label className="mr-2 text-sm font-medium">Humidity</label>
        <input
          type="number"
          className="mr-2 w-16 rounded border border-gray-300 px-2 py-1 text-sm"
          placeholder="From"
          value={humidityFrom}
          onChange={(e) => setHumidityFrom(e.target.value)}
        />
        <input
          type="number"
          className="w-16 rounded border border-gray-300 px-2 py-1 text-sm"
          placeholder="To"
          value={humidityTo}
          onChange={(e) => setHumidityTo(e.target.value)}
        />
      </div>

      {/* Action Buttons */}
      <div className="mt-4 flex justify-end">
        <button
          onClick={handleSubmit}
          className="mr-2 rounded bg-blue-500 px-4 py-1 text-sm font-semibold text-white hover:bg-blue-600"
        >
          Submit
        </button>
        <button
          onClick={handleClear}
          className="rounded bg-gray-300 px-4 py-1 text-sm font-semibold text-gray-800 hover:bg-gray-400"
        >
          Clear
        </button>
      </div>
    </div>
  );
};

export default FilterDataComponent;
