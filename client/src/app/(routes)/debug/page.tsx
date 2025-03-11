"use client";

import { getDataService } from "@/app/services/dataService";
import { getSensorService } from "@/app/services/sensorService";
import { SensorDataParams, SensorParams } from "@/types";
import { useState } from "react";

const Debug = () => {
  const [startDate, setStartDate] = useState<Date>();
  const [endDate, setEndDate] = useState<Date>();

  const submitDates = async (e: React.SyntheticEvent<HTMLFormElement>) => {
    e.preventDefault();
    const date = e.currentTarget.startDate.value;
    console.log(date);
    console.log(typeof date);
    // setStartDate(new Date(e.currentTarget.startDate.value));
    // setEndDate(new Date(e.currentTarget.endDate.value));

    // if (!startDate || !endDate) return;

    // console.log("action");
    // await testPostAction(startDate, endDate);
  };

  const testGet = async () => {
    console.log("test");
    console.log();
    const testParams: SensorParams = {
      id: "24E124136E106616",
    };

    const res = await getSensorService(testParams);
    console.log(res);
  };

  const dataService = async () => {
    const testParams: SensorDataParams = {
      sensor_id: "24E124136E106616",
    };

    const res = await getDataService(testParams);
    console.log(res);
  };

  return (
    <div className="">
      <button onClick={testGet}>TEST</button>

      <h2>Dates</h2>
      <div className="flex gap-4">
        <form
          className="flex w-1/4 flex-col"
          onSubmit={submitDates}
        >
          <label>Start date</label>
          <input
            name="startDate"
            type="datetime-local"
          />

          <label>End date</label>
          <input
            name="endDate"
            type="date"
          />

          <button
            className="bg-blue mt-2 w-fit rounded-md p-2 text-white"
            type="submit"
          >
            Submit
          </button>
        </form>

        <div>
          <h2>Start date</h2>
          <div>{startDate?.toISOString().split("T")[0]}</div>
          <h2>End date</h2>
          <div>{endDate?.toISOString().split("T")[0]}</div>
        </div>
      </div>
      <button onClick={testGet}>Test Get</button>

      <button onClick={dataService}>getDataService</button>
    </div>
  );
};

export default Debug;
