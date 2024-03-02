"use client";
import { useState } from "react";
import ObjectViewer from "./object-viewer";

const api = "http://localhost:8000";

export default function Home() {
  const [object, setObject] = useState<string | null>(null);
  const [prompt, setPrompt] = useState<string>("a sphere");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  // make a request to the backend to generate an object
  const generate = async (prompt: string) => {
    setLoading(true);
    const res = await fetch(`${api}/prompt/${prompt}`);
    setLoading(false);
    const object = await res.text();
    if (!object.endsWith(".obj")) setError(object);
    else setObject(object);
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm">
        <div className="flex justify-center p-4">
          <img src="/gen3d_black.png" className="w-24" alt="Gen3D" />
        </div>
        <div className="flex justify-center mt-4">
          <input
            placeholder="Generate anything"
            className="max-w-full w-64 p-4 py-2 rounded"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
          />
          <button
            className="border border-gray-00 rounded text-xl px-2 bg-gray-500"
            disabled={loading}
            onClick={() => !loading && generate(prompt)}
          >
            ✨
          </button>
        </div>
        <div className="border border-gray-500 mt-8 rounded-xl">
          {object ? (
            <ObjectViewer object={object} />
          ) : error ? (
            <div className="p-4">{error}</div>
          ) : (
            <div className="p-4">Loading...</div>
          )}
        </div>
      </div>
    </main>
  );
}
