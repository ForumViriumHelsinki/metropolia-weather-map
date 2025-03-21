import { capitalize } from "./capitalize";

export function fixLocation(input: string): string {
  if (input === "makelankatu") {
    return capitalize(input.slice(0, 1) + "ä" + input.slice(2));
  }
  return input;
}
