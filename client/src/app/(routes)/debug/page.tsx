import { apiFetch } from "@/utils/apiFetch";
import ClientDebug from "./ClientDebug";

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
