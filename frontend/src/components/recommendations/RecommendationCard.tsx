import React from 'react';
import { Sparkles, Calendar, BadgeAlert } from 'lucide-react';
import { Recommendation } from '../../types/prediction';
import { cn } from '../../lib/utils';

interface RecommendationCardProps {
  recommendation: Recommendation;
  isOriginal?: boolean;
}

export const RecommendationCard: React.FC<RecommendationCardProps> = ({
  recommendation,
  isOriginal = false
}) => {
  const getPriorityBadge = (p: string) => {
    switch (p) {
      case 'HIGH':
        return 'bg-red-50 border-red-100 text-red-700';
      case 'MEDIUM':
        return 'bg-amber-50 border-amber-100 text-amber-700';
      default:
        return 'bg-blue-50 border-blue-100 text-blue-700';
    }
  };

  return (
    <div className={cn(
      "bg-white p-6 rounded-2xl border shadow-sm space-y-5",
      isOriginal ? "border-slate-200" : "border-blue-100 bg-blue-50/5"
    )}>
      <div className="flex items-center justify-between border-b border-slate-100 pb-3">
        <div className="flex items-center gap-2">
          <Sparkles className="h-5 w-5 text-blue-500 shrink-0" />
          <h4 className="font-bold text-slate-800 text-sm tracking-wide">
            {isOriginal ? 'AI Recommended Program' : 'Intervention Recommendation'}
          </h4>
        </div>
        <span className={cn(
          "px-2.5 py-0.5 border text-[10px] font-bold rounded-md uppercase tracking-wider",
          getPriorityBadge(recommendation.priority)
        )}>
          {recommendation.priority} Priority
        </span>
      </div>

      <div className="space-y-4">
        <div>
          <h3 className="font-extrabold text-slate-800 text-lg tracking-tight">{recommendation.title}</h3>
          <p className="text-xs text-slate-500 font-medium leading-relaxed mt-2">{recommendation.summary}</p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 border-t border-slate-100 pt-4 text-xs font-semibold">
          <div>
            <span className="text-[10px] text-slate-400 uppercase tracking-wider block mb-1">Review Period</span>
            <div className="flex items-center gap-1.5 text-slate-700">
              <Calendar className="h-4.5 w-4.5 text-blue-500" />
              <span>{recommendation.review_period_days} Days</span>
            </div>
          </div>

          <div>
            <span className="text-[10px] text-slate-400 uppercase tracking-wider block mb-1">Reasoning Model</span>
            <div className="flex items-center gap-1.5 text-slate-700">
              <BadgeAlert className="h-4.5 w-4.5 text-blue-500" />
              <span className="font-mono text-[11px] bg-slate-100 px-2 py-0.5 border rounded border-slate-200">{recommendation.llm_model}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
