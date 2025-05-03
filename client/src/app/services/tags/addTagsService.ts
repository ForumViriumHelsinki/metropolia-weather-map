import { Sensor } from "@/types";
import { apiFetch } from "@/utils/apiFetch";

export const addTagService = async (sensors: Sensor[], tag: string) => {
  try {
    const body = JSON.stringify({
      ids: sensors.map((s) => s.id),
      tag,
    });

    const res = await apiFetch("/sensor-tags", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body,
    });

    if (!res.ok) {
      const errorData = await res.json();
      throw new Error("Error adding tag to sensor", errorData.detail);
    }

    return await res.json();
  } catch (error) {
    console.error("Error adding tag to sensors");
    throw error;
  }
};
