import { apiFetch } from "@/utils/apiFetch";

export interface TagGraphParams {
  tag1: string;
  tag2: string;
  graph_type: GraphTypes;
  location?: Locations | null;
  startDate?: string | null;
  endDate?: string | null;
  timeOfDay?: TimeOfDay;
  analysis_variable?: AnalysisType;
}
export enum GraphTypes {
  Bar = "bar",
  Plot = "plot",
}
export enum Locations {
  vallilla = "Vallila",
  laajasalo = "Laajasalo",
  koivukyla = "Koivukyla",
}

export enum TimeOfDay {
  WholeDay = "whole day",
  Daytime = "daytime",
  Nighttime = "nighttime",
}

export enum AnalysisType {
  Temperature = "temperature",
  Humidity = "humidity",
}

const toSnakeCase = (str: string): string =>
  str.replace(/[A-Z]/g, (letter) => `_${letter.toLowerCase()}`);

export const getTagGraphService = async (
  params: TagGraphParams,
): Promise<Blob> => {
  console.log(params);
  try {
    const searchParams = new URLSearchParams();
    for (const [key, val] of Object.entries(params)) {
      console.log(key, val);
      if (!val) continue;

      searchParams.set(toSnakeCase(key), val);
    }

    console.log(searchParams.toString());
    const res = await apiFetch(
      `/analysis/temperature?${searchParams.toString()}`,
    );

    if (!res.ok) {
      const errorData = await res.json();
      console.error(errorData);
      throw new Error(errorData.detail);
    }

    const data = await res.blob();
    return data;
  } catch (error) {
    console.error("Error fetching graph", error);
    throw error;
  }
};
