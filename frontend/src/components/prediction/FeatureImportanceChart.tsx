import React from 'react';
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  Cell, 
  Tooltip, 
  ResponsiveContainer,
  ReferenceLine,
  CartesianGrid
} from 'recharts';

interface FeatureImportanceChartProps {
  shapValues: Record<string, number>;
}

export const FeatureImportanceChart: React.FC<FeatureImportanceChartProps> = ({ shapValues }) => {
  // 1. Convert to sorted array of key-value pairs
  const chartData = Object.entries(shapValues)
    .map(([key, val]) => {
      // Clean names
      let displayName = key
        .replace('_yes', '')
        .replace('_no', ' (No)')
        .replace('schoolsup', 'School Support')
        .replace('famsup', 'Family Support')
        .replace('studytime', 'Study Time')
        .replace('failures', 'Class Failures')
        .replace('absences', 'School Absences')
        .replace('alc_consumption', 'Alcohol Intake')
        .replace('grade_trend', 'Grade Change')
        .replace('study_to_free_ratio', 'Free vs Study time')
        .replace('parent_edu_sum', 'Parents Education')
        .replace('internet', 'Internet Access')
        .replace('romantic', 'Romantic Status')
        .replace('famrel', 'Family Relations')
        .replace('freetime', 'Free Time')
        .replace('goout', 'Going Out')
        .replace('health', 'Health Index')
        .replace('traveltime', 'Travel Time');
        
      return {
        rawName: key,
        name: displayName,
        value: Number(val.toFixed(4)),
      };
    })
    // Sort by absolute influence value
    .sort((a, b) => Math.abs(b.value) - Math.abs(a.value))
    // Take top 8 contributors
    .slice(0, 8)
    // Reverse for bottom-to-top layout
    .reverse();

  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      const dataPoint = payload[0].payload;
      const isPositive = dataPoint.value > 0;
      return (
        <div className="bg-slate-900 text-slate-100 p-2.5 rounded-lg shadow-lg border border-slate-800 text-xs font-semibold">
          <p className="font-bold text-sm mb-1">{dataPoint.name}</p>
          <p>SHAP Value: <span className={isPositive ? 'text-red-400' : 'text-emerald-400'}>{dataPoint.value}</span></p>
          <p className="text-[10px] text-slate-400 font-semibold mt-1">
            {isPositive 
              ? 'Increases risk classification' 
              : 'Protects / decreases risk classification'}
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm flex flex-col h-[340px]">
      <h4 className="text-sm font-semibold text-slate-500 uppercase tracking-wide mb-1">SHAP Explainable AI Matrix</h4>
      <p className="text-[10px] text-slate-400 font-semibold mb-4">Top contributors pushing risk level direction (G1/G2 included if late-stage)</p>
      
      <div className="flex-1 min-h-0">
        {chartData.length === 0 ? (
          <div className="h-full flex items-center justify-center text-slate-400 text-sm">
            No SHAP factors calculated yet.
          </div>
        ) : (
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={chartData}
              layout="vertical"
              margin={{ top: 5, right: 10, left: 10, bottom: 5 }}
            >
              <CartesianGrid strokeDasharray="3 3" stroke="#F1F5F9" horizontal={false} />
              <XAxis type="number" stroke="#94A3B8" fontSize={9} />
              <YAxis 
                dataKey="name" 
                type="category" 
                stroke="#94A3B8" 
                fontSize={9} 
                width={100}
                tickLine={false} 
              />
              <Tooltip content={<CustomTooltip />} cursor={{ fill: '#F8FAFC' }} />
              <ReferenceLine x={0} stroke="#94A3B8" strokeWidth={1} />
              <Bar 
                dataKey="value" 
                radius={[4, 4, 4, 4]}
              >
                {chartData.map((entry, index) => {
                  const isPositive = entry.value > 0;
                  return (
                    <Cell 
                      key={`cell-${index}`} 
                      fill={isPositive ? '#F87171' : '#34D399'} // soft red for positive, soft green for negative
                    />
                  );
                })}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        )}
      </div>
    </div>
  );
};
