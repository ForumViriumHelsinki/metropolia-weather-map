import { SensorType } from "@/types";
import { apiFetch } from "@/utils/apiFetch";

export const GET = async (
  _req: Request,
  { params }: { params: Promise<{ type: SensorType }> },
) => {
  const type = (await params).type;
  const res = await apiFetch(`/sensors/type/${type}`);
  const data = await res.json();

  return Response.json(data);
};
