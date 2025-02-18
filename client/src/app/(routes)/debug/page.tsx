"use client";

import { testGetAction, testPostAction } from "@/app/actions/debugAction";
import { useState } from "react";

const Debug = () => {
  const [startDate, setStartDate] = useState<Date>();
  const [endDate, setEndDate] = useState<Date>();

  const submitDates = async (e: React.SyntheticEvent<HTMLFormElement>) => {
    e.preventDefault();
    setStartDate(new Date(e.currentTarget.startDate.value));
    setEndDate(new Date(e.currentTarget.endDate.value));

    if (!startDate || !endDate) return;

    console.log("action");
    await testPostAction(startDate, endDate);
  };

  const testGet = async () => {
    const res = await testGetAction();
  };

  return (
    <div className="">
      <h2>Dates</h2>
      <div className="flex gap-4">
        <form
          className="flex w-1/4 flex-col"
          onSubmit={submitDates}
        >
          <label>Start date</label>
          <input
            name="startDate"
            type="date"
          />

          <label>End date</label>
          <input
            name="endDate"
            type="date"
          />

          <button
            className="mt-2 w-fit rounded-md bg-blue p-2 text-white"
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
    </div>
  );
};

export default Debug;
