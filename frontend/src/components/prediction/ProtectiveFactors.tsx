import React from 'react';
import { ShieldAlert, CheckCircle2 } from 'lucide-react';

interface ProtectiveFactorsProps {
  factors: string[];
}

export const ProtectiveFactors: React.FC<ProtectiveFactorsProps> = ({ factors }) => {
  return (
    <div className="bg-white p-6 rounded-2xl border border-emerald-50/60 shadow-sm flex flex-col space-y-4">
      <div className="flex items-center gap-2 text-emerald-700">
        <CheckCircle2 className="h-5 w-5 text-emerald-500" />
        <h4 className="font-bold text-sm uppercase tracking-wide">Protective Elements</h4>
      </div>
      
      {factors.length === 0 ? (
        <p className="text-slate-400 text-xs font-semibold">No significant protective assets cataloged.</p>
      ) : (
        <ul className="space-y-2">
          {factors.map((factor, index) => (
            <li 
              key={index}
              className="flex items-start gap-2.5 p-2 bg-emerald-50/50 border border-emerald-50 text-slate-700 rounded-xl text-xs font-medium"
            >
              <CheckCircle2 className="h-4 w-4 text-emerald-400 shrink-0 mt-0.5" />
              <span>{factor}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};
