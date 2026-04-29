import React from 'react';
import { Video, AlertCircle, Eye, Settings } from 'lucide-react';
import CameraGrid from './components/CameraGrid';
import EventsList from './components/EventsList';
import AlertsPanel from './components/AlertsPanel';
import StatsCard from './components/StatsCard';

const Dashboard: React.FC = () => {
  const [activeTab, setActiveTab] = React.useState<'cameras' | 'events' | 'alerts' | 'stats'>('cameras');

  return (
    <div className="min-h-screen bg-slate-900 text-white">
      {/* Header */}
      <header className="bg-slate-800 border-b border-slate-700 p-6">
        <div className="max-w-7xl mx-auto">
          <h1 className="text-3xl font-bold flex items-center gap-2">
            <Video className="text-blue-400" />
            Video Analytics Platform
          </h1>
          <p className="text-slate-400 mt-1">Real-time object detection and event analysis</p>
        </div>
      </header>

      {/* Navigation */}
      <nav className="bg-slate-800 border-b border-slate-700 sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-6 flex gap-8">
          {[
            { id: 'cameras', label: 'Cameras', icon: Eye },
            { id: 'events', label: 'Events', icon: AlertCircle },
            { id: 'alerts', label: 'Alerts', icon: AlertCircle },
            { id: 'stats', label: 'Statistics', icon: Settings }
          ].map(({ id, label, icon: Icon }) => (
            <button
              key={id}
              onClick={() => setActiveTab(id as any)}
              className={`py-4 px-2 border-b-2 transition flex items-center gap-2 ${
                activeTab === id
                  ? 'border-blue-400 text-blue-400'
                  : 'border-transparent text-slate-400 hover:text-white'
              }`}
            >
              <Icon size={20} />
              {label}
            </button>
          ))}
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto p-6">
        {activeTab === 'cameras' && <CameraGrid />}
        {activeTab === 'events' && <EventsList />}
        {activeTab === 'alerts' && <AlertsPanel />}
        {activeTab === 'stats' && (
          <div className="grid grid-cols-4 gap-6">
            <StatsCard title="Active Cameras" value="4" change="+1" icon="📹" />
            <StatsCard title="Total Detections" value="2.5K" change="+12%" icon="👁️" />
            <StatsCard title="Events Today" value="28" change="+5" icon="⚠️" />
            <StatsCard title="Active Alerts" value="3" change="-1" icon="🔔" />
          </div>
        )}
      </main>
    </div>
  );
};

export default Dashboard;
