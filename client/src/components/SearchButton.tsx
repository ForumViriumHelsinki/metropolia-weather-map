"use client";

export default function SearchButton() {
  return (
    <button
      className="rounded-md bg-blue-500 px-4 py-2 text-white"
      onClick={() => {
        console.log("Search button clicked");
      }}
    >
      Search
    </button>
  );
}
