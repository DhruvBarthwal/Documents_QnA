"use client";
import { useState, useEffect, useRef } from "react";

const STAGES = ["parsing", "cleaning", "chunking", "embedding", "indexing"];

const FileUpload = ({ onUploaded }: { onUploaded: (chunks: number) => void }) => {
  const [status, setStatus] = useState<"idle" | "processing" | "ready" | "error">("idle");
  const [stage, setStage] = useState("");
  const [chunks, setChunks] = useState(0);
  const intervalRef = useRef<NodeJS.Timeout | null>(null);

  async function handleFile(file: File) {
    setStatus("processing");
    setStage("parsing");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://localhost:8000/upload", {
        method: "POST",
        body: formData,
      });
      const { file_id } = await res.json();

      // Poll status
      intervalRef.current = setInterval(async () => {
        const statusRes = await fetch(`http://localhost:8000/status/${file_id}`);
        const data = await statusRes.json();

        if (data.status === "ready") {
          clearInterval(intervalRef.current!);
          setStatus("ready");
          setChunks(data.chunks);
          onUploaded(data.chunks);
        } else if (data.status === "error") {
          clearInterval(intervalRef.current!);
          setStatus("error");
        } else {
          setStage(data.stage || "processing");
        }
      }, 1000);

    } catch (e) {
      setStatus("error");
    }
  }

  useEffect(() => () => {
    if (intervalRef.current) clearInterval(intervalRef.current);
  }, []);

  const progress = stage
    ? Math.round(((STAGES.indexOf(stage) + 1) / STAGES.length) * 100)
    : 10;

  return (
    <div className="mt-5 w-full flex justify-center">
      {status === "idle" && (
        <div
          className="border-2 w-120 border-dashed rounded-lg p-6 text-center cursor-pointer hover:border-blue-400 transition-colors"
          onDragOver={(e) => e.preventDefault()}
          onDrop={(e) => {
            e.preventDefault();
            if (e.dataTransfer.files[0]) handleFile(e.dataTransfer.files[0]);
          }}
        >
          <input
            type="file"
            className="hidden"
            id="fileInput"
            onChange={(e) => e.target.files && handleFile(e.target.files[0])}
          />
          <label htmlFor="fileInput" className="cursor-pointer text-white">
            Drag & drop PDF or click to upload
          </label>
        </div>
      )}

      {/* Progress Bar */}
      {status === "processing" && (
        <div className="rounded-lg w-100 border p-4">
          <div className="flex justify-between text-sm text-white mb-2">
            <span className="capitalize font-medium">{stage}...</span>
            <span>{progress}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="bg-blue-500 h-2 rounded-full transition-all duration-700"
              style={{ width: `${progress}%` }}
            />
          </div>
          <p className="text-xs text-gray-400 mt-2">
            Step {STAGES.indexOf(stage) + 1} of {STAGES.length}
          </p>
        </div>
      )}

      {/* Ready */}
      {status === "ready" && (
        <div className="rounded-lg w-120  border border-green-200 bg-gray-900 p-4 flex items-center justify-between">
          <p className=" text-lg pl-20 font-medium">
             Your file is ready!
          </p>
          <button
            className="text-md bg-gray-700 border border-2px p-5 rounded-md"
            onClick={() => setStatus("idle")}
          >
            Upload another
          </button>
        </div>
      )}

      {/* Error */}
      {status === "error" && (
        <div className="rounded-lg border border-red-200 bg-red-50 p-4 flex items-center justify-between">
          <p className="text-red-600 text-sm"> Processing failed</p>
          <button
            className="text-xs text-gray-400 hover:text-gray-600"
            onClick={() => setStatus("idle")}
          >
            Try again
          </button>
        </div>
      )}
    </div>
  );
};

export default FileUpload;