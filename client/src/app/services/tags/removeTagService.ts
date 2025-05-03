import { Sensor } from "@/types";
import { apiFetch } from "@/utils/apiFetch";

export const removeTagService = async (sensors: Sensor[], tag: string) => {
  try {
    const res = await apiFetch("/sensor-tags", {
      method: "Delete",
      body: JSON.stringify({
        ids: sensors.map((s) => s.id),
        tag: tag,
      }),
      headers: { "Content-Type": "application/json" },
    });

    if (!res.ok) {
      const errorData = await res.json();
      throw new Error("Error removing tag", errorData.detail);
    }

    return await res.json();
  } catch (error) {
    throw error;
  }
};
