import React from 'react';
import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { RiskDistributionItem } from '../../api/analytics';

interface RiskDistributionChartProps {
  data: RiskDistributionItem[];
}

const COLORS = {
  LOW_RISK: '#10B981',    // Emerald Green
  MEDIUM_RISK: '#F59E0B', // Amber Yellow
  HIGH_RISK: '#EF4444',   // Bright Red
};

export const RiskDistributionChart: React.FC<RiskDistributionChartProps> = ({ data }) => {
  // Format data for chart
  const chartData = data.map(item => ({
    name: item.risk_level.replace('_', ' '),
    value: item.count,
    percentage: item.percentage,
    key: item.risk_level
  }));

  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      const dataPoint = payload[0].payload;
      return (
        <div className="bg-slate-900 text-slate-100 p-3 rounded-lg shadow-lg border border-slate-800 text-xs font-semibold">
          <p className="font-bold text-sm mb-1">{dataPoint.name}</p>
          <p>Count: {dataPoint.value} Students</p>
          <p>Share: {dataPoint.percentage}%</p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm flex flex-col h-[360px]">
      <h3 className="font-bold text-slate-800 text-base mb-4">Academic Risk Distribution</h3>
      <div className="flex-1 min-h-0">
        {chartData.length === 0 || chartData.every(c => c.value === 0) ? (
          <div className="h-full flex items-center justify-center text-slate-400 text-sm">
            No risk assessment records recorded yet.
          </div>
        ) : (
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={chartData}
                cx="50%"
                cy="50%"
                innerRadius={65}
                outerRadius={95}
                paddingAngle={4}
                dataKey="value"
              >
                {chartData.map((entry, index) => (
                  <Cell 
                    key={`cell-${index}`} 
                    fill={COLORS[entry.key as keyof typeof COLORS] || '#718096'} 
                  />
                ))}
              </Pie>
              <Tooltip content={<CustomTooltip />} />
              <Legend 
                verticalAlign="bottom" 
                height={36} 
                iconType="circle"
                iconSize={8}
                formatter={(value) => <span className="text-xs font-semibold text-slate-500 capitalize">{value.toLowerCase()}</span>}
              />
            </PieChart>
          </ResponsiveContainer>
        )}
      </div>
    </div>
  );
};
