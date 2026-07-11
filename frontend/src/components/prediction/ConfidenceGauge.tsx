import React from 'react';

interface ConfidenceGaugeProps {
  confidence: number;
}

export const ConfidenceGauge: React.FC<ConfidenceGaugeProps> = ({ confidence }) => {
  const percentage = Math.round(confidence * 100);
  const strokeDashoffset = 251.2 - (251.2 * percentage) / 100;

  const getGaugeColor = (pct: number) => {
    if (pct >= 80) return 'stroke-emerald-500';
    if (pct >= 50) return 'stroke-amber-500';
    return 'stroke-red-500';
  };

  const getGaugeBg = (pct: number) => {
    if (pct >= 80) return 'text-emerald-500 bg-emerald-50';
    if (pct >= 50) return 'text-amber-500 bg-amber-50';
    return 'text-red-500 bg-red-50';
  };

  const color = getGaugeColor(percentage);
  const bg = getGaugeBg(percentage);

  return (
    <div className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm flex flex-col items-center justify-center text-center h-[260px]">
      <h4 className="text-sm font-semibold text-slate-500 uppercase tracking-wide mb-4">ANN Model Confidence</h4>
      
      <div className="relative flex items-center justify-center h-32 w-32">
        <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
          {/* Background circle */}
          <circle
            className="stroke-slate-100"
            strokeWidth="8"
            fill="transparent"
            r="40"
            cx="50"
            cy="50"
          />
          {/* Progress circle */}
          <circle
            className={`${color} transition-all duration-1000 ease-out`}
            strokeWidth="8"
            strokeDasharray="251.2"
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            fill="transparent"
            r="40"
            cx="50"
            cy="50"
          />
        </svg>
        <div className="absolute flex flex-col items-center">
          <span className="text-3xl font-black text-slate-800 tracking-tight">{percentage}%</span>
          <span className="text-[9px] text-slate-400 font-bold uppercase tracking-wider">Confidence</span>
        </div>
      </div>
      
      <span className={`mt-4 px-3 py-1 text-[10px] font-bold tracking-wide rounded-full border border-current ${bg}`}>
        {percentage >= 80 ? 'High certainty' : (percentage >= 50 ? 'Moderate certainty' : 'Low certainty')}
      </span>
    </div>
  );
};
