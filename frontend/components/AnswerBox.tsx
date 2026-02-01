import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

export default function AnswerBox({
  answer,
  latency,
}: {
  answer: string;
  latency: number;
}) {
  if (!answer) return null;

  return (
    <div className="mt-6 w-250 p-4 text-lg rounded">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          h1: ({ node, ...props }) => (
            <h1 className="text-3xl font-bold mt-4 mb-2" {...props} />
          ),
          h2: ({ node, ...props }) => (
            <h2 className="text-xl font-semibold mt-3 mb-2" {...props} />
          ),
          h3: ({ node, ...props }) => (
            <h3 className="text-lg font-semibold  mt-3 mb-2" {...props} />
          ),
          strong: ({ node, ...props }) => (
            <strong className="font-semibold text-xl " {...props} />
          ),
          p: ({ ...props }) => (
            <p className="mb-4 leading-relaxed" {...props} />
          ),
          ul: ({ node, ...props }) => (
            <ul className="list-disc pl-6 my-2 text-lg" {...props} />
          ),
          ol: ({ node, ...props }) => (
            <ol className="list-decimal pl-6 my-2 text-lg" {...props} />
          ),
          li: ({ node, ...props }) => (
            <li className="mb-1 text-lg" {...props} />
          ),
        }}
      >
        {answer}
      </ReactMarkdown>

      <div className="text-sm text-gray-500 mt-3">
        ⏱ {latency.toFixed(1)} ms
      </div>
    </div>
  );
}
