"use client";

import { TempData } from "@/app/page";
import { useState } from "react";

// Transitions have to be nested to allow for separate transition timings and durations

const SensorInfo = ({ data }: { data: TempData }) => {
  const [visible, setVisible] = useState<boolean>(false);
  const bgColor = visible ? "bg-[#F2BB0A]" : "bg-yellow";

  return (
    <div
      className="relative [&>div]:duration-500 [&_h4]:text-xl [&_h4]:font-roman"
      onClick={() => setVisible((v) => !v)}
    >
      <div
        className={`${visible ? "sensor-info-shadow" : ""} relative text-black transition-all`}
      >
        <div
          className={`${bgColor} px-6 py-2 transition-colors duration-300 ease-linear`}
        >
          <h3 className="text-2xl font-medium">Sensori</h3>
          <div className="grid grid-cols-2 text-xl">
            <span>{data.temperature}°C</span>
            <span>{data.humidity}%</span>
          </div>
        </div>
      </div>

      {/* Details */}
      <div
        //
        className={`absolute top-[calc(100%-6px)] h-fit overflow-hidden transition-all ${visible ? "sensor-info-shadow max-h-[150px]" : "max-h-0"} w-full text-black [&_span]:text-lg`}
      >
        <div
          className={`${bgColor} px-6 pb-2 transition-colors duration-300 ease-linear`}
        >
          <div>
            <h4>Sijainti</h4>
            <span>{data.type}</span>
          </div>
          <div>
            <h4>Kiinnitys</h4>
            <span>{data.attached}</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SensorInfo;
