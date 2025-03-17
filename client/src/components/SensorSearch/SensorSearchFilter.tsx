"use client";

import { useState } from "react";
import { SensorFilter } from "../types";

const filterFields: { key: string; label: string; type: string }[] = [
  { key: "dateRange", label: "Date Range", type: "datetime-local" },
  { key: "attachedTo", label: "Attached To", type: "text" },
  { key: "type", label: "Type", type: "text" },
  { key: "note", label: "Note", type: "text" },
];

export default function SensorSearchFilter() {
  const [checkedState, setCheckedState] = useState<{
    [key in keyof SensorFilter]?: boolean;
  }>({});
  const [values, setValues] = useState<SensorFilter>({});

  const handleCheckboxChange = (key: string) => {
    if (checkedState[key as keyof SensorFilter]) {
      setValues((prev) => ({ ...prev, [key]: undefined })); // Reset value if unchecked
    }
    setCheckedState((prev) => ({
      ...prev,
      [key as keyof SensorFilter]: !prev[key as keyof SensorFilter],
    }));
  };

  const handleInputChange = (
    key: string,
    value: string | number,
    isEndValue = false,
  ) => {
    setValues((prev) => {
      if (key === "dateRange" && typeof value === "string") {
        const [start, end] = prev.dateRange || ["", ""];
        return {
          ...prev,
          dateRange: isEndValue ? [start, value] : [value, end],
        };
      }
      return { ...prev, [key]: value };
    });
  };

  const handleSubmit = async () => {
    console.log("Filter Values:", values);
    // Further processing logic here
    const params = new URLSearchParams();
    Object.entries(values).forEach(([key, value]) => {
      if (value !== undefined) {
        if (Array.isArray(value)) {
          params.append("start_date", value[0]);
          params.append("end_date", value[1]);
        } else {
          if (key === "attachedTo") {
            params.append("attached", value as string);
          } else if (key === "type") {
            params.append("type", value as string);
          } else if (key === "note") {
            params.append("note", value as string);
          }
        }
      }
    });
    const url = "http://localhost:8000/api/sensors/?" + params.toString();

    try {
      const res = await fetch(url);
      if (!res.ok) {
        throw new Error("Failed to fetch sensors");
      }
      const data = await res.json();
      console.log(data);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div
      style={{
        width: 500,
        padding: "20px",
        background: "white",
        boxShadow: "0px 0px 5px 2px rgba(0, 0, 0, 0.25)",
        overflow: "hidden",
        flexDirection: "column",
        justifyContent: "flex-start",
        alignItems: "center",
        gap: 20,
        display: "flex",
      }}
    >
      <div style={{ fontSize: 24, fontWeight: "bold", color: "black" }}>
        Filters
      </div>

      <div
        style={{
          width: "100%",
          flexDirection: "column",
          gap: 10,
          display: "flex",
        }}
      >
        {filterFields.map(({ key, label, type }) => (
          <div
            key={key}
            style={{ display: "flex", alignItems: "center", gap: 10 }}
          >
            <input
              type="checkbox"
              id={`${key}-checkbox`}
              checked={checkedState[key as keyof SensorFilter] || false}
              onChange={() => handleCheckboxChange(key)}
              style={{ width: 20, height: 20 }}
            />
            <label
              htmlFor={`${key}-checkbox`}
              style={{
                fontSize: 14,
                color: "black",
                opacity: checkedState[key as keyof SensorFilter] ? 1 : 0.5,
              }}
            >
              {label}
            </label>

            {type === "datetime-local" && key === "dateRange" ? (
              <>
                <input
                  type="datetime-local"
                  id={`${key}-start`}
                  name={`${key}-start`}
                  disabled={!checkedState[key]}
                  value={values[key as keyof SensorFilter]?.[0] || ""}
                  onChange={(e) => handleInputChange(key, e.target.value)}
                  style={{
                    width: 170,
                    padding: "4px",
                    borderRadius: 4,
                    border: "1px solid #9BA1A6",
                    opacity: checkedState[key] ? 1 : 0.5,
                  }}
                />
                <input
                  type="datetime-local"
                  id={`${key}-end`}
                  name={`${key}-end`}
                  disabled={!checkedState[key]}
                  value={values[key as keyof SensorFilter]?.[1] || ""}
                  onChange={(e) => handleInputChange(key, e.target.value, true)}
                  style={{
                    width: 170,
                    padding: "4px",
                    borderRadius: 4,
                    border: "1px solid #9BA1A6",
                    opacity: checkedState[key] ? 1 : 0.5,
                  }}
                />
              </>
            ) : (
              <input
                type={type}
                id={key}
                name={key}
                placeholder={label}
                value={values[key as keyof SensorFilter] || ""}
                disabled={!checkedState[key as keyof SensorFilter]}
                onChange={(e) =>
                  handleInputChange(
                    key,
                    type === "number" ? Number(e.target.value) : e.target.value,
                  )
                }
                style={{
                  width: 150,
                  height: 30,
                  borderRadius: 4,
                  border: "1px solid #9BA1A6",
                  padding: "4px",
                  opacity: checkedState[key as keyof SensorFilter] ? 1 : 0.5,
                }}
              />
            )}
          </div>
        ))}
      </div>

      <div style={{ display: "flex", gap: 15 }}>
        <button
          onClick={handleSubmit}
          style={{
            width: 100,
            height: 40,
            background: "#007BFF",
            borderRadius: 6,
            color: "white",
            fontSize: 16,
            fontWeight: "bold",
            border: "none",
            cursor: "pointer",
          }}
        >
          Submit
        </button>
        <button
          style={{
            width: 100,
            height: 40,
            background: "#D9D9D9",
            borderRadius: 6,
            color: "black",
            fontSize: 16,
            fontWeight: "bold",
            border: "none",
            cursor: "pointer",
          }}
        >
          Cancel
        </button>
      </div>
    </div>
  );
}
