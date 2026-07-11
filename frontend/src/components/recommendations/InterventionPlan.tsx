import React from 'react';
import { CheckSquare, Eye, Award } from 'lucide-react';

interface InterventionPlanProps {
  recommendedActions: string[];
  monitoringPlan: string[];
  successIndicators: string[];
}

export const InterventionPlan: React.FC<InterventionPlanProps> = ({
  recommendedActions,
  monitoringPlan,
  successIndicators
}) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      {/* Recommended Actions */}
      <div className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm space-y-4">
        <div className="flex items-center gap-2 text-blue-700">
          <CheckSquare className="h-5 w-5 text-blue-500" />
          <h4 className="font-bold text-sm uppercase tracking-wide">Action Steps</h4>
        </div>
        <ul className="space-y-3.5">
          {recommendedActions.map((action, idx) => (
            <li key={idx} className="flex items-start gap-2.5 text-xs text-slate-600 font-semibold leading-relaxed">
              <span className="h-5 w-5 rounded-lg bg-blue-50 text-blue-600 text-[10px] font-bold flex items-center justify-center shrink-0 mt-0.5">
                {idx + 1}
              </span>
              <span>{action}</span>
            </li>
          ))}
        </ul>
      </div>

      {/* Monitoring Plan */}
      <div className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm space-y-4">
        <div className="flex items-center gap-2 text-indigo-700">
          <Eye className="h-5 w-5 text-indigo-500" />
          <h4 className="font-bold text-sm uppercase tracking-wide">Monitoring Plan</h4>
        </div>
        <ul className="space-y-3.5">
          {monitoringPlan.map((step, idx) => (
            <li key={idx} className="flex items-start gap-2.5 text-xs text-slate-600 font-semibold leading-relaxed">
              <span className="h-5 w-5 rounded-lg bg-indigo-50 text-indigo-600 text-[10px] font-bold flex items-center justify-center shrink-0 mt-0.5">
                {idx + 1}
              </span>
              <span>{step}</span>
            </li>
          ))}
        </ul>
      </div>

      {/* Success Indicators */}
      <div className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm space-y-4">
        <div className="flex items-center gap-2 text-emerald-700">
          <Award className="h-5 w-5 text-emerald-500" />
          <h4 className="font-bold text-sm uppercase tracking-wide">Success Indicators</h4>
        </div>
        <ul className="space-y-3.5">
          {successIndicators.map((indicator, idx) => (
            <li key={idx} className="flex items-start gap-2.5 text-xs text-slate-600 font-semibold leading-relaxed">
              <span className="h-5 w-5 rounded-lg bg-emerald-50 text-emerald-600 text-[10px] font-bold flex items-center justify-center shrink-0 mt-0.5">
                {idx + 1}
              </span>
              <span>{indicator}</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};
