"use client";

import { TempData } from "@/app/page";
import { useState } from "react";

const SensorInfo = ({ data }: { data: TempData }) => {
  const [visible, setVisible] = useState<boolean>(false);
  const bgColor = visible ? "bg-[#F2BB0A]" : "bg-yellow";

  return (
    <div
      className="relative [&>div]:px-6 [&>div]:duration-500 [&>div]:ease-linear [&_h4]:text-xl [&_h4]:font-roman"
      onClick={() => setVisible((v) => !v)}
    >
      <div
        className={`${bgColor} ${visible ? "sensor-info-shadow" : ""} relative h-fit py-2 text-black transition-all`}
      >
        <h3 className="text-2xl font-medium">Sensori</h3>
        <div className="grid grid-cols-2 text-xl">
          <span>{data.temperature}°C</span>
          <span>{data.humidity}%</span>
        </div>
      </div>

      {/* Details */}
      <div
        className={`${bgColor} absolute top-[calc(100%-8px)] h-fit overflow-hidden transition-all ${visible ? "sensor-info-shadow max-h-[150px] pb-2" : "max-h-0 pb-0"} w-full text-black [&_span]:text-lg`}
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
  );
};

export default SensorInfo;
