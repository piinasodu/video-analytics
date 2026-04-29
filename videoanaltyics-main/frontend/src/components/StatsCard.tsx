import React from 'react';

interface StatsCardProps {
  title: string;
  value: string;
  change: string;
  icon: string;
}

const StatsCard: React.FC<StatsCardProps> = ({ title, value, change, icon }) => {
  const isPositive = !change.startsWith('-');

  return (
    <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-slate-400 text-sm font-medium">{title}</p>
          <h3 className="text-3xl font-bold text-white mt-2">{value}</h3>
          <p className={`text-sm mt-2 ${isPositive ? 'text-green-400' : 'text-red-400'}`}>
            {change}
          </p>
        </div>
        <div className="text-4xl">{icon}</div>
      </div>
    </div>
  );
};

export default StatsCard;
