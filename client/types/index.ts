export enum SensorType {
  "auringossa",
  "varjossa",
}

export type Sensor = {
  id: string;
  location: [number, number];
  type: SensorType;
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
