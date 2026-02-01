"use client";
import { useState } from "react";
import { uploadfile } from "@/lib/api";

const FileUpload = ({ onUploaded }: { onUploaded: () => void }) => {
  const [loading, setLoading] = useState(false);

  async function handleFile(file: File) {
    setLoading(true);
    try {
      await uploadfile(file);
      onUploaded();
    } catch (e) {
      alert("Upload failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div
      className="border-2 border-dashed rounded-lg p-6 mt-5 text-center cursor-pointer"
      onDragOver={(e) => e.preventDefault()}
      onDrop={(e) => {
        e.preventDefault();
        if (e.dataTransfer.files[0]) {
          handleFile(e.dataTransfer.files[0]);
        }
      }}
    >
      <input
        type="file"
        className="hidden"
        id="fileInput"
        onChange={(e) => e.target.files && handleFile(e.target.files[0])}
      />

      <label htmlFor="fileInput" className="cursor-pointer">
        {loading ? "Uploading..." : "Drag & drop PDF or click to upload"}
      </label>
    </div>
  );
};

export default FileUpload;
