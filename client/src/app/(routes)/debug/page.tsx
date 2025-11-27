import { apiFetch } from "@/utils/apiFetch";
import ClientDebug from "./ClientDebug";

// Force dynamic rendering since this page fetches data from the API
export const dynamic = 'force-dynamic';

const Debug = async () => {
  // const res = await fetch("http://python-server:8000/api/sensors");
  const res = await apiFetch("/sensors");
  console.log(await res.json());

  return (
    <div>
      <ClientDebug />
      <></>
    </div>
  );
};

export default Debug;
