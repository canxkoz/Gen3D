"use client";
import { Canvas, useLoader } from "@react-three/fiber";
import { Environment, OrbitControls, useGLTF } from "@react-three/drei";
import { OBJLoader } from "three/addons/loaders/OBJLoader.js";

function Model({ url }: { url: string }) {
  // const { scene } = useGLTF(url);
  const scene = useLoader(OBJLoader, url);
  return <primitive object={scene} />;
}

export default function ObjectViewer({ object }: { object: string }) {
  return (
    <div style={{ height: 500 }}>
      <Canvas>
        <OrbitControls />
        <ambientLight intensity={Math.PI / 2} />
        <pointLight position={[10, 10, 10]} />
        <Model url={object} />
        <Environment preset="sunset" /> {/* Example of adding an environment */}
      </Canvas>
    </div>
  );
}
