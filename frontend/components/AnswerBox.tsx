"use client";
import { useState, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

export default function AnswerBox({
  answer,
  latency,
}: {
  answer: string;
  latency: number;
}) {
  const [displayed, setDisplayed] = useState("");

  useEffect(() => {
    setDisplayed("");
    if (!answer) return;

    let i = 0;
    const interval = setInterval(() => {
      setDisplayed(answer.slice(0, i + 1));
      i++;
      if (i >= answer.length) clearInterval(interval);
    }, 10); // ← speed: lower = faster

    return () => clearInterval(interval);
  }, [answer]);

  if (!answer) return null;

  return (
    <div className="mt-6 w-250 p-4 pb-8 bg-gray-900 text-lg rounded">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          h1: ({ ...props }) => <h1 className="text-3xl font-bold mt-4 mb-2" {...props} />,
          h2: ({ ...props }) => <h2 className="text-xl font-semibold mt-3 mb-2" {...props} />,
          h3: ({ ...props }) => <h3 className="text-lg font-semibold mt-3 mb-2" {...props} />,
          strong: ({ ...props }) => <strong className="font-semibold text-xl" {...props} />,
          p: ({ ...props }) => <p className="mb-4 leading-relaxed" {...props} />,
          ul: ({ ...props }) => <ul className="list-disc pl-6 my-2 text-lg" {...props} />,
          ol: ({ ...props }) => <ol className="list-decimal pl-6 my-2 text-lg" {...props} />,
          li: ({ ...props }) => <li className="mb-1 text-lg" {...props} />,
        }}
      >
        {displayed}
      </ReactMarkdown>

      {displayed === answer && (
        <div className="text-md text-gray-500 mt-3">
          Another query? Ask away!
        </div>
      )}
    </div>
  );
}