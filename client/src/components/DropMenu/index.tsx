"use client";

import { ReactNode, useEffect, useRef, useState } from "react";

const DropMenu = ({
  title,
  children,
}: {
  title: string;
  children: ReactNode;
}) => {
  const [expand, setExpand] = useState<boolean>(false);
  const [collapsedHeight, setCollapsedHeight] = useState<number | undefined>(
    undefined,
  );
  const [rotation, setRotation] = useState<number>(90);
  const contentRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (contentRef.current) {
      const firstChild = contentRef.current.firstElementChild as HTMLElement;
      if (firstChild) {
        setCollapsedHeight(
          firstChild.offsetHeight + 24
        );
      }
    }
  }, [children]);

  const handleClick = () => {
    setExpand(!expand);
    setRotation((prev) => prev + 180);
  };

  return (
    <div
      className="flex flex-col overflow-hidden"
      onClick={handleClick}
    >
      <div className="flex w-full rounded-tl-lg text-2xl">
        <div className="flex w-fit">
          <h2 className="bg-off-white rounded-tl-lg py-3 pl-4">{title}</h2>
          <div
            className={`bg-off-white rounded-tr-lg py-3 font-bold duration-300 select-none`}
          >
            <div
              className="px-4 duration-300"
              style={{
                transform: `rotate(${rotation}deg)`,
              }}
            >
              &gt;
            </div>
          </div>
        </div>

        {/* Rounded corners between divs */}
        <div className="relative flex w-full">
          <div className="bg-off-white w-full"></div>
          <div className="bg-blue-m absolute h-full w-full rounded-bl-lg py-3"></div>
        </div>
      </div>

      <div
        ref={contentRef}
        style={{
          maxHeight: expand
            ? contentRef.current?.scrollHeight
            : collapsedHeight,
        }}
        className="box-basic grid-scaling transform overflow-hidden rounded-tl-none transition-[max-height] duration-300 ease-in-out bg-off-white"
      >
        {children}
      </div>
    </div>
  );
};

export default DropMenu;
