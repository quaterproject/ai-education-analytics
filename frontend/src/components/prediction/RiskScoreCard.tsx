import React from 'react';
import { AlertCircle, ShieldAlert, CheckCircle2, Info } from 'lucide-react';
import { cn } from '../../lib/utils';

interface RiskScoreCardProps {
  riskLevel: 'LOW_RISK' | 'MEDIUM_RISK' | 'HIGH_RISK';
  confidence: number;
}

export const RiskScoreCard: React.FC<RiskScoreCardProps> = ({ riskLevel, confidence }) => {
  const getRiskDetails = () => {
    switch (riskLevel) {
      case 'HIGH_RISK':
        return {
          title: 'High Academic Risk',
          description: 'The student exhibits serious warning signals in multiple indicators, such as absences, class failures, and early grades. Immediate educator intervention is strongly recommended.',
          colorClass: 'bg-red-50 border-red-100 text-red-800',
          icon: ShieldAlert,
          iconColorClass: 'text-red-500',
        };
      case 'MEDIUM_RISK':
        return {
          title: 'Medium Academic Risk',
          description: 'The student shows borderline academic indicators. Attendance rates or assignments are declining. Periodic checks and localized academic support (like tutoring) are advised.',
          colorClass: 'bg-amber-50 border-amber-100 text-amber-800',
          icon: AlertCircle,
          iconColorClass: 'text-amber-500',
        };
      default:
        return {
          title: 'Low Academic Risk',
          description: 'The student is performing well and shows stable attendance patterns. Maintain standard teaching support and regular check-ins.',
          colorClass: 'bg-emerald-50 border-emerald-100 text-emerald-800',
          icon: CheckCircle2,
          iconColorClass: 'text-emerald-500',
        };
    }
  };

  const details = getRiskDetails();
  const Icon = details.icon;

  return (
    <div className="space-y-4">
      {/* Risk Banner */}
      <div className={cn(
        "p-6 rounded-2xl border flex items-start gap-4 shadow-sm",
        details.colorClass
      )}>
        <div className={cn("p-2 bg-white rounded-xl shadow-sm", details.iconColorClass)}>
          <Icon className="h-7 w-7" />
        </div>
        <div className="space-y-1">
          <h3 className="text-lg font-bold tracking-tight">{details.title}</h3>
          <p className="text-sm leading-relaxed opacity-90">{details.description}</p>
          <div className="pt-2 text-xs font-bold opacity-75">
            ANN Prediction Confidence: {Math.round(confidence * 100)}%
          </div>
        </div>
      </div>

      {/* Mandatory Decision Support Disclaimer */}
      <div className="p-4 bg-slate-50 border border-slate-200 rounded-xl flex items-center gap-3 text-slate-500">
        <Info className="h-5 w-5 text-blue-500 shrink-0" />
        <p className="text-xs font-semibold leading-relaxed">
          <b>Disclaimer:</b> AI predictions are decision-support recommendations and require educator review. 
          Final academic intervention decisions remain the responsibility of qualified personnel.
        </p>
      </div>
    </div>
  );
};
