import { useRef, useState } from "react";

export const useMessageDisplay = () => {
  const [message, setMessage] = useState<string>("");
  const timeoutRef = useRef<NodeJS.Timeout | null>(null);

  const displayMessage = (message: string) => {
    setMessage(message);

    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
    }

    timeoutRef.current = setTimeout(() => {
      setMessage("");
    }, 3000);
  };

  return [message, displayMessage] as const;
};
