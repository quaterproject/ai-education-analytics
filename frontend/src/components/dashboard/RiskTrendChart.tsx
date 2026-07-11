import React from 'react';
import { 
  AreaChart, 
  Area, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  Legend, 
  ResponsiveContainer 
} from 'recharts';
import { RiskTrendItem } from '../../api/analytics';

interface RiskTrendChartProps {
  data: RiskTrendItem[];
}

export const RiskTrendChart: React.FC<RiskTrendChartProps> = ({ data }) => {
  // Format dates for friendly display
  const chartData = data.map(item => {
    try {
      const date = new Date(item.date);
      return {
        ...item,
        formattedDate: date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
      };
    } catch {
      return {
        ...item,
        formattedDate: item.date
      };
    }
  });

  return (
    <div className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm flex flex-col h-[360px]">
      <h3 className="font-bold text-slate-800 text-base mb-4">Risk Trends Over Time</h3>
      <div className="flex-1 min-h-0">
        {data.length === 0 ? (
          <div className="h-full flex items-center justify-center text-slate-400 text-sm">
            No history trend records available.
          </div>
        ) : (
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart
              data={chartData}
              margin={{ top: 10, right: 10, left: -20, bottom: 0 }}
            >
              <defs>
                <linearGradient id="colorHigh" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#EF4444" stopOpacity={0.2}/>
                  <stop offset="95%" stopColor="#EF4444" stopOpacity={0.01}/>
                </linearGradient>
                <linearGradient id="colorMedium" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#F59E0B" stopOpacity={0.2}/>
                  <stop offset="95%" stopColor="#F59E0B" stopOpacity={0.01}/>
                </linearGradient>
                <linearGradient id="colorLow" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#10B981" stopOpacity={0.2}/>
                  <stop offset="95%" stopColor="#10B981" stopOpacity={0.01}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#F1F5F9" />
              <XAxis 
                dataKey="formattedDate" 
                stroke="#94A3B8" 
                fontSize={10} 
                tickLine={false} 
              />
              <YAxis 
                stroke="#94A3B8" 
                fontSize={10} 
                tickLine={false} 
                allowDecimals={false}
              />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: '#0F172A', 
                  border: 'none', 
                  borderRadius: '8px', 
                  color: '#F8FAFC',
                  fontSize: '11px' 
                }} 
              />
              <Legend 
                verticalAlign="top" 
                height={36} 
                iconType="circle"
                iconSize={8}
                formatter={(value) => <span className="text-xs font-semibold text-slate-500 capitalize">{value.replace('_', ' ').toLowerCase()}</span>}
              />
              <Area 
                type="monotone" 
                dataKey="high_risk" 
                stroke="#EF4444" 
                fillOpacity={1} 
                fill="url(#colorHigh)" 
                strokeWidth={2}
              />
              <Area 
                type="monotone" 
                dataKey="medium_risk" 
                stroke="#F59E0B" 
                fillOpacity={1} 
                fill="url(#colorMedium)" 
                strokeWidth={2}
              />
              <Area 
                type="monotone" 
                dataKey="low_risk" 
                stroke="#10B981" 
                fillOpacity={1} 
                fill="url(#colorLow)" 
                strokeWidth={2}
              />
            </AreaChart>
          </ResponsiveContainer>
        )}
      </div>
    </div>
  );
};
