"use client";
import { Canvas } from "@react-three/fiber";
import { Environment, OrbitControls, useGLTF } from "@react-three/drei";

function Model({ url }: { url: string }) {
  const { scene } = useGLTF(url);
  return <primitive object={scene} />;
}

export default function ObjectViewer() {
  return (
    <div style={{ height: 500 }}>
      <Canvas>
        <OrbitControls />
        <ambientLight intensity={Math.PI / 2} />
        <pointLight position={[10, 10, 10]} />
        <Model url="/3d_cake.glb" />
        <Environment preset="sunset" /> {/* Example of adding an environment */}
      </Canvas>
    </div>
  );
}
