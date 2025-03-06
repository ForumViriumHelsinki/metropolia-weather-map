import { apiFetch } from "@/utils/apiFetch";

export const getSensorsService = async () => {
  const res = await apiFetch("/sensors/");
  return await res.json();
};
