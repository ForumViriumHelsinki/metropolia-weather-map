export type Sensor = {
  id: string;
  location: [number, number];
  type: "Auringossa" | "Varjossa" | undefined;
  note: string | null;
  attached: string;
  installDate: Date;
};

export type SensorData = {
  id: number;
  time: Date;
  humidity: number;
  temperature: number;
  sensor: string;
};

export interface SensorParams {
  id?: string;
  location?: [number, number];
  type?: string;
  note?: string;
  attached?: string;
  install_date_from?: string;
  install_date_to?: string;
  fields?: string[];
}

export interface SensorDataParams {
  sensor_id?: string;
  start_date?: string;
  end_date?: string;
  humidity_from?: number;
  humidity_to?: number;
  temperature_from?: number;
  temperature_to?: number;
}
