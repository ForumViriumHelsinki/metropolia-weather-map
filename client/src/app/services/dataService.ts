import { SensorDataParams } from "@/types";
import { apiFetch } from "@/utils/apiFetch";

export const getDataService = async (params: SensorDataParams) => {
  const urlParams = new URLSearchParams();

  Object.entries(params).forEach(([key, value]) => {
    if (value) {
      urlParams.append(key, value);
    }
  });

  const res = await apiFetch(`/sensordata?${urlParams.toString()}`);
  const data = await res.json();
  console.log(data);
};
