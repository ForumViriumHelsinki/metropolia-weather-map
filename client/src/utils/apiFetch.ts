export const apiFetch = async (
  endpoint: string,
  options?: RequestInit,
): Promise<Response> => {
  const res = await fetch(
    `${process.env.NEXT_PUBLIC_PYTHON_API}/api${endpoint}`,
    options,
  );
  return res;
};
