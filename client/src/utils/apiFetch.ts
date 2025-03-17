export const apiFetch = async (
  endpoint: string,
  options?: RequestInit,
): Promise<Response> => {
  let url: string;

  if (!process.env.NEXT_PUBLIC_CLIENT_API) {
    // Use only localhost for fetching if not ran in Docker
    const res = await fetch(
      `${process.env.NEXT_PUBLIC_PYTHON_API}/api${endpoint}`,
      options,
    );

    return res;
  }

  if (typeof window === "undefined") {
    // Server component fetch
    url = process.env.NEXT_PUBLIC_PYTHON_API!;
  } else {
    // Client component fetch
    url = process.env.NEXT_PUBLIC_CLIENT_API!;
  }

  const res = await fetch(`${url}/api${endpoint}`, options);
  return res;
};

export const checkClient = () => {
  if (typeof window === "undefined") console.log("server");
  else console.log("client");
};
