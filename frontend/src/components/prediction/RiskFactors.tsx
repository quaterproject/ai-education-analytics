import React from 'react';
import { AlertCircle, AlertTriangle } from 'lucide-react';

interface RiskFactorsProps {
  factors: string[];
}

export const RiskFactors: React.FC<RiskFactorsProps> = ({ factors }) => {
  return (
    <div className="bg-white p-6 rounded-2xl border border-red-50/60 shadow-sm flex flex-col space-y-4">
      <div className="flex items-center gap-2 text-red-700">
        <AlertCircle className="h-5 w-5 text-red-500" />
        <h4 className="font-bold text-sm uppercase tracking-wide">Key Risk Drivers</h4>
      </div>
      
      {factors.length === 0 ? (
        <p className="text-slate-400 text-xs font-semibold">No critical risk factors registered.</p>
      ) : (
        <ul className="space-y-2">
          {factors.map((factor, index) => (
            <li 
              key={index}
              className="flex items-start gap-2.5 p-2 bg-red-50/50 border border-red-50 text-slate-700 rounded-xl text-xs font-medium"
            >
              <AlertTriangle className="h-4 w-4 text-red-400 shrink-0 mt-0.5" />
              <span>{factor}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};
