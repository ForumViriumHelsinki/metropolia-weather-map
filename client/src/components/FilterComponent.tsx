'use client'

import { useState } from "react";
import { SensorSearchFilter } from "../types";


const filterFields: { key: string; label: string; type: string }[] = [
    { key: "dateRange", label: "Date Range", type: "datetime-local" },
    { key: "installed", label: "Installed Date", type: "datetime-local" },
    { key: "attachedTo", label: "Attached To", type: "text" },
    { key: "type", label: "Type", type: "text" },
    { key: "note", label: "Note", type: "text" },
    { key: "tempRange", label: "Temperature Range", type: "number" },
    { key: "humidityRange", label: "Humidity Range", type: "number" },
];

export default function FilterComponent() {
    const [checkedState, setCheckedState] = useState<{ [key in keyof SensorSearchFilter]?: boolean }>({});
    const [values, setValues] = useState<SensorSearchFilter>({});

    const handleCheckboxChange = (key: string) => {
        if (checkedState[key]) {
            setValues((prev) => ({ ...prev, [key]: undefined })); // Reset value if unchecked
        }
        setCheckedState((prev) => ({ ...prev, [key]: !prev[key] }));
    };

    const handleInputChange = (key: string, value: string | number, isEndValue = false) => {
        setValues((prev) => {
            if (key === "dateRange" && typeof value === "string") {
                const [start, end] = prev.dateRange || ["", ""];
                return { ...prev, dateRange: isEndValue ? [start, value] : [value, end] };
            }
            if ((key === "tempRange" || key === "humidityRange") && typeof value === "number") {
                const [min, max] = prev[key] || [0, 0];
                return { ...prev, [key]: isEndValue ? [min, value] : [value, max] };
            }
            return { ...prev, [key]: value };
        });
    };

    const handleSubmit = () => {
        console.log("Filter Values:", values);
        // Further processing logic here
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
            <div style={{ fontSize: 24, fontWeight: "bold", color: "black" }}>Filters</div>

            <div style={{ width: "100%", flexDirection: "column", gap: 10, display: "flex" }}>
                {filterFields.map(({ key, label, type }) => (
                    <div key={key} style={{ display: "flex", alignItems: "center", gap: 10 }}>
                        <input
                            type="checkbox"
                            id={`${key}-checkbox`}
                            checked={checkedState[key] || false}
                            onChange={() => handleCheckboxChange(key)}
                            style={{ width: 20, height: 20 }}
                        />
                        <label
                            htmlFor={`${key}-checkbox`}
                            style={{
                                fontSize: 14,
                                color: "black",
                                opacity: checkedState[key] ? 1 : 0.5,
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
                        ) : key === "tempRange" || key === "humidityRange" ? (
                            <>
                                <input
                                    type="number"
                                    id={`${key}-min`}
                                    name={`${key}-min`}
                                    placeholder="Min"
                                    disabled={!checkedState[key]}
                                    onChange={(e) => handleInputChange(key, Number(e.target.value))}
                                    style={{
                                        width: 70,
                                        height: 30,
                                        borderRadius: 4,
                                        border: "1px solid #9BA1A6",
                                        padding: "4px",
                                        opacity: checkedState[key] ? 1 : 0.5,
                                    }}
                                />
                                <input
                                    type="number"
                                    id={`${key}-max`}
                                    name={`${key}-max`}
                                    placeholder="Max"
                                    disabled={!checkedState[key]}
                                    onChange={(e) => handleInputChange(key, Number(e.target.value), true)}
                                    style={{
                                        width: 70,
                                        height: 30,
                                        borderRadius: 4,
                                        border: "1px solid #9BA1A6",
                                        padding: "4px",
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
                                disabled={!checkedState[key]}
                                onChange={(e) =>
                                    handleInputChange(
                                        key,
                                        type === "number" ? Number(e.target.value) : e.target.value
                                    )
                                }
                                style={{
                                    width: 150,
                                    height: 30,
                                    borderRadius: 4,
                                    border: "1px solid #9BA1A6",
                                    padding: "4px",
                                    opacity: checkedState[key] ? 1 : 0.5,
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
