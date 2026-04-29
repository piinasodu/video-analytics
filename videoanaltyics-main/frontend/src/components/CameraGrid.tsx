import React from 'react';
import { Play, Pause, Settings } from 'lucide-react';

interface CameraProps {
  id: string;
  name: string;
  status: 'online' | 'offline';
  fps: number;
  detections: number;
}

const CameraCard: React.FC<CameraProps> = ({ id, name, status, fps, detections }) => {
  const [isPlaying, setIsPlaying] = React.useState(false);

  return (
    <div className="bg-slate-800 rounded-lg overflow-hidden border border-slate-700 hover:border-slate-600 transition">
      {/* Video Feed */}
      <div className="aspect-video bg-black relative group">
        <div className="absolute inset-0 flex items-center justify-center bg-gradient-to-br from-slate-900 to-black">
          <Play className="w-16 h-16 text-slate-400" />
        </div>
        
        {/* Status Badge */}
        <div className="absolute top-2 right-2">
          <span className={`px-2 py-1 rounded text-xs font-semibold ${
            status === 'online'
              ? 'bg-green-900 text-green-200'
              : 'bg-red-900 text-red-200'
          }`}>
            {status.toUpperCase()}
          </span>
        </div>

        {/* Controls */}
        <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black to-transparent p-4 opacity-0 group-hover:opacity-100 transition flex gap-2">
          <button className="bg-blue-600 hover:bg-blue-700 p-2 rounded text-white">
            {isPlaying ? <Pause size={20} /> : <Play size={20} />}
          </button>
          <button className="bg-slate-700 hover:bg-slate-600 p-2 rounded text-white ml-auto">
            <Settings size={20} />
          </button>
        </div>
      </div>

      {/* Info */}
      <div className="p-4 space-y-2">
        <h3 className="font-semibold text-white">{name}</h3>
        <div className="grid grid-cols-2 gap-2 text-sm">
          <div className="bg-slate-700 rounded p-2">
            <p className="text-slate-400">FPS</p>
            <p className="text-white font-semibold">{fps}</p>
          </div>
          <div className="bg-slate-700 rounded p-2">
            <p className="text-slate-400">Detections</p>
            <p className="text-white font-semibold">{detections}</p>
          </div>
        </div>
      </div>
    </div>
  );
};

const CameraGrid: React.FC = () => {
  const cameras: CameraProps[] = [
    { id: '1', name: 'Main Entrance', status: 'online', fps: 30, detections: 15 },
    { id: '2', name: 'Parking Lot', status: 'online', fps: 30, detections: 8 },
    { id: '3', name: 'Hallway', status: 'online', fps: 25, detections: 3 },
    { id: '4', name: 'Back Door', status: 'offline', fps: 0, detections: 0 },
  ];

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold">Live Cameras</h2>
        <button className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded font-semibold">
          + Add Camera
        </button>
      </div>

      <div className="grid grid-cols-2 gap-6">
        {cameras.map(camera => (
          <CameraCard key={camera.id} {...camera} />
        ))}
      </div>
    </div>
  );
};

export default CameraGrid;
