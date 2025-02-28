import { apiFetch } from "@/utils/apiFetch";
import { NextRequest } from "next/server";

export const GET = async (req: NextRequest) => {
  const searchParams = req.nextUrl.searchParams;
  const startDate = searchParams.get("start_date");
  const endDate = searchParams.get("end_date");

  if (!startDate || !endDate) {
    return Response.json({ error: "Missing params" }, { status: 400 });
  }

  const params = new URLSearchParams({
    start_date: startDate,
    end_date: endDate,
  });

  const res = await apiFetch(`/sensordata/dates?${params}`);
  const data = await res.json();

  return Response.json(data);
};
