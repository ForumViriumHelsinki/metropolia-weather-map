import { apiFetch } from "@/utils/apiFetch";

export const GET = async (
  _req: Request,
  { params }: { params: Promise<{ id: string }> },
) => {
  const id = (await params).id;
  const res = await apiFetch(`/sensors/id/${id}`);
  const data = await res.json();

  return Response.json(data);
};
