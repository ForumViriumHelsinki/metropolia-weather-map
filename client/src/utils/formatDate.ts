export const formatDate = (date: Date) => {
  const str = date.toString();
  const day = str.slice(0, 10);
  const time = str.slice(11, 16);
  return `${time} - ${day}`;
};
