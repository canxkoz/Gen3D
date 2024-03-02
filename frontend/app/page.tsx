import Image from "next/image";
import ObjectViewer from "./object-viewer";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm">
        <div className="flex justify-center p-4">
          <img src="/gen3d_black.png" className="w-24" />
        </div>
        <div className="flex justify-center mt-4">
          <input
            placeholder="Generate anything"
            className="max-w-full w-64 p-4 py-2 rounded"
          />
          <button className="border border-gray-00 rounded text-xl px-2 bg-gray-500">
            ✨
          </button>
        </div>
        <div className="border border-gray-500 mt-8 rounded-xl">
          <ObjectViewer />
        </div>
      </div>
    </main>
  );
}
