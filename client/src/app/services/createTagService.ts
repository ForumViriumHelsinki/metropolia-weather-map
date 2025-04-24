import { apiFetch } from "@/utils/apiFetch";

export const createTagService = async (newTag: string) => {
  try {
    const res = await apiFetch("/tags", {
      method: "POST",
      body: JSON.stringify({ tag: newTag }),
      headers: { "Content-Type": "application/json" },
    });

    if (!res.ok) {
      const errorData = await res.json();
      throw new Error("Error creating new tag", errorData);
    }

    return await res.json();
  } catch (error) {
    console.error("Error creating new tag", error);
    throw error;
  }
};
