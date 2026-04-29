import React from 'react';
import { AlertTriangle, AlertCircle, Info, CheckCircle } from 'lucide-react';

interface Event {
  id: string;
  camera: string;
  type: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  timestamp: string;
  description: string;
  status: 'open' | 'acknowledged' | 'resolved';
}

const EventsList: React.FC = () => {
  const [events] = React.useState<Event[]>([
    {
      id: '1',
      camera: 'Main Entrance',
      type: 'crowd_detected',
      severity: 'high',
      timestamp: '2026-04-17 14:23:45',
      description: '15 people detected in entrance area',
      status: 'open'
    },
    {
      id: '2',
      camera: 'Parking Lot',
      type: 'vehicle_detected',
      severity: 'low',
      timestamp: '2026-04-17 14:20:12',
      description: 'Vehicle entered parking lot',
      status: 'acknowledged'
    },
    {
      id: '3',
      camera: 'Hallway',
      type: 'intrusion_detected',
      severity: 'critical',
      timestamp: '2026-04-17 14:15:33',
      description: 'Person detected in restricted zone',
      status: 'resolved'
    }
  ]);

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical':
        return 'bg-red-900 text-red-200';
      case 'high':
        return 'bg-orange-900 text-orange-200';
      case 'medium':
        return 'bg-yellow-900 text-yellow-200';
      default:
        return 'bg-blue-900 text-blue-200';
    }
  };

  const getSeverityIcon = (severity: string) => {
    switch (severity) {
      case 'critical':
      case 'high':
        return <AlertTriangle className="text-red-400" size={20} />;
      case 'medium':
        return <AlertCircle className="text-yellow-400" size={20} />;
      default:
        return <Info className="text-blue-400" size={20} />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'open':
        return 'text-red-400';
      case 'acknowledged':
        return 'text-yellow-400';
      case 'resolved':
        return 'text-green-400';
      default:
        return 'text-slate-400';
    }
  };

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold">Recent Events</h2>

      <div className="space-y-4">
        {events.map(event => (
          <div
            key={event.id}
            className="bg-slate-800 rounded-lg p-6 border border-slate-700 hover:border-slate-600 transition"
          >
            <div className="flex items-start justify-between">
              <div className="flex items-start gap-4 flex-1">
                {getSeverityIcon(event.severity)}
                <div className="flex-1">
                  <div className="flex items-center gap-3">
                    <h3 className="text-lg font-semibold">
                      {event.type.replace(/_/g, ' ').toUpperCase()}
                    </h3>
                    <span className={`px-3 py-1 rounded text-sm font-semibold ${getSeverityColor(event.severity)}`}>
                      {event.severity.toUpperCase()}
                    </span>
                    <span className={`px-3 py-1 rounded text-sm font-semibold ml-auto ${getStatusColor(event.status)}`}>
                      {event.status.toUpperCase()}
                    </span>
                  </div>
                  <p className="text-slate-400 mt-1">Camera: {event.camera}</p>
                  <p className="text-white mt-2">{event.description}</p>
                  <p className="text-slate-500 text-sm mt-2">{event.timestamp}</p>
                </div>
              </div>
              <button className="ml-4 bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded font-semibold whitespace-nowrap">
                View
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default EventsList;
