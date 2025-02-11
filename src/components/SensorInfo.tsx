"use client";

import { TempData } from "@/app/page";
import { useState } from "react";

const SensorInfo = ({ data }: { data: TempData }) => {
  const [visible, setVisible] = useState<boolean>(false);
  const bgColor = visible ? "bg-red-300" : "bg-yellow";

  return (
    <div className="relative [&_h4]:text-xl [&_h4]:font-roman">
      <div
        className={`${bgColor} ${!visible && "pb-2"} px-6 pt-2 text-black`}
        onClick={() => setVisible((v) => !v)}
      >
        <div className="">
          <h3 className="text-2xl font-medium">Sensori</h3>
          <div className="grid grid-cols-2 text-xl">
            <span>{data.temperature}°C</span>
            <span>{data.humidity}%</span>
          </div>
        </div>
      </div>

      {visible && (
        <div
          className={`${bgColor} absolute z-20 w-full px-6 pb-2 text-black [&_span]:text-lg`}
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
      )}
    </div>
  );
};

export default SensorInfo;
