import React from 'react';
import { Bell, Trash2, Edit } from 'lucide-react';

interface Alert {
  id: string;
  rule: string;
  type: string;
  status: 'active' | 'acknowledged' | 'resolved';
  triggered: number;
  lastTriggered: string;
}

const AlertsPanel: React.FC = () => {
  const [alerts] = React.useState<Alert[]>([
    {
      id: '1',
      rule: 'High Crowd Alert',
      type: 'crowd_detected',
      status: 'active',
      triggered: 5,
      lastTriggered: '2026-04-17 14:23:45'
    },
    {
      id: '2',
      rule: 'Intrusion Detection',
      type: 'intrusion_detected',
      status: 'active',
      triggered: 1,
      lastTriggered: '2026-04-17 14:15:33'
    },
    {
      id: '3',
      rule: 'Vehicle Entry',
      type: 'vehicle_detected',
      status: 'acknowledged',
      triggered: 12,
      lastTriggered: '2026-04-17 14:10:00'
    }
  ]);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return 'bg-red-900 text-red-200';
      case 'acknowledged':
        return 'bg-yellow-900 text-yellow-200';
      case 'resolved':
        return 'bg-green-900 text-green-200';
      default:
        return 'bg-slate-700 text-slate-200';
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold">Alert Rules</h2>
        <button className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded font-semibold">
          + New Alert
        </button>
      </div>

      <div className="grid gap-4">
        {alerts.map(alert => (
          <div
            key={alert.id}
            className="bg-slate-800 rounded-lg p-6 border border-slate-700 hover:border-slate-600 transition"
          >
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-4 flex-1">
                <Bell className="text-blue-400" size={24} />
                <div>
                  <h3 className="text-lg font-semibold">{alert.rule}</h3>
                  <p className="text-slate-400">Type: {alert.type}</p>
                </div>
              </div>
              <div className="flex items-center gap-4">
                <div className="text-right">
                  <p className="text-2xl font-bold text-white">{alert.triggered}</p>
                  <p className="text-slate-400 text-sm">Triggered</p>
                </div>
                <span className={`px-3 py-1 rounded text-sm font-semibold ${getStatusColor(alert.status)}`}>
                  {alert.status.toUpperCase()}
                </span>
                <div className="flex gap-2">
                  <button className="bg-slate-700 hover:bg-slate-600 p-2 rounded text-white">
                    <Edit size={18} />
                  </button>
                  <button className="bg-red-900 hover:bg-red-800 p-2 rounded text-white">
                    <Trash2 size={18} />
                  </button>
                </div>
              </div>
            </div>
            <p className="text-slate-400 text-sm mt-3">Last triggered: {alert.lastTriggered}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default AlertsPanel;
