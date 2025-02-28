import { apiFetch } from "@/utils/apiFetch";

export const GET = async () => {
  const res = await apiFetch("/sensors");
  const data = await res.json();

  return Response.json(data);
};

// TODO: Implementation not finished
export const POST = async (newSensor: any) => {
  const res = await apiFetch("/sensors", {
    method: "POST",
    body: JSON.stringify(newSensor),
  });
  const data = await res.json();

  return Response.json({ message: "Implementation not finished" });
  return Response.json(data);
};
