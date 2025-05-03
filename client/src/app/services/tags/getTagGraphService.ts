import { GraphTypes, Locations } from "@/types";
import { apiFetch } from "@/utils/apiFetch";

export interface TagGraphParams {
  tag1: string;
  tag2: string;
  graph_type: GraphTypes;
  location?: Locations | null;
  start_date?: string | null;
  end_date?: string | null;
  daytime?: boolean;
  nighttime?: boolean;
}

export const getTagGraphService = async (
  params: TagGraphParams,
): Promise<Blob> => {
  try {
    const searchParams = new URLSearchParams();
    for (const [key, val] of Object.entries(params)) {
      if (!val) continue;

      searchParams.set(key, val);
    }

    const res = await apiFetch(
      `/analysis/temperature?${searchParams.toString()}`,
    );

    if (!res.ok) {
      const errorData = await res.json();
      console.error(errorData);
      throw new Error("Error creating data", errorData.detail);
    }

    const data = await res.blob();
    return data;
  } catch (error) {
    console.error("Error fetching graph", error);
    throw error;
  }
};
