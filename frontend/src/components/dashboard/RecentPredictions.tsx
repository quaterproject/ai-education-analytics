import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, AlertTriangle, CheckCircle2, AlertCircle } from 'lucide-react';
import { Prediction } from '../../types/prediction';

interface RecentPredictionsProps {
  predictions: Array<Prediction & { student_name: string; student_code: string }>;
}

export const RecentPredictions: React.FC<RecentPredictionsProps> = ({ predictions }) => {
  const getRiskBadge = (level: string) => {
    switch (level) {
      case 'HIGH_RISK':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-1 bg-red-50 border border-red-100 text-red-700 text-xs font-semibold rounded-full">
            <AlertOctagon className="h-3 w-3" />
            <span>High Risk</span>
          </span>
        );
      case 'MEDIUM_RISK':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-1 bg-amber-50 border border-amber-100 text-amber-700 text-xs font-semibold rounded-full">
            <AlertTriangle className="h-3 w-3" />
            <span>Medium Risk</span>
          </span>
        );
      default:
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-1 bg-emerald-50 border border-emerald-100 text-emerald-700 text-xs font-semibold rounded-full">
            <CheckCircle2 className="h-3 w-3" />
            <span>Low Risk</span>
          </span>
        );
    }
  };

  return (
    <div className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm flex flex-col h-[360px]">
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-bold text-slate-800 text-base">Recent Predictions</h3>
        <Link 
          to="/students" 
          className="text-xs font-semibold text-blue-600 hover:text-blue-700 flex items-center gap-1.5 transition-colors duration-200"
        >
          <span>View Registry</span>
          <ArrowRight className="h-3.5 w-3.5" />
        </Link>
      </div>

      <div className="flex-1 overflow-y-auto pr-1">
        {predictions.length === 0 ? (
          <div className="h-full flex items-center justify-center text-slate-400 text-sm">
            No recent predictions found.
          </div>
        ) : (
          <div className="space-y-3">
            {predictions.map((pred) => (
              <div 
                key={pred.id} 
                className="flex items-center justify-between p-3.5 bg-slate-50 rounded-xl hover:bg-slate-100/70 transition-colors duration-200 border border-transparent hover:border-slate-100"
              >
                <div>
                  <h4 className="font-bold text-sm text-slate-700">{pred.student_name}</h4>
                  <span className="text-xs text-slate-400 font-semibold">{pred.student_code} • {new Date(pred.created_at).toLocaleDateString()}</span>
                </div>
                <div className="flex items-center gap-4">
                  <div className="text-right">
                    <p className="text-xs font-bold text-slate-500">{getRiskBadge(pred.risk_level)}</p>
                    <span className="text-[10px] text-slate-400 font-bold">Conf: {Math.round(pred.confidence * 100)}%</span>
                  </div>
                  <Link 
                    to={`/students/${pred.student_id}`}
                    className="p-1.5 bg-white border border-slate-200 rounded-lg text-slate-400 hover:text-slate-600 hover:border-slate-300 transition-colors duration-200 shadow-sm"
                  >
                    <ArrowRight className="h-4 w-4" />
                  </Link>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

// Quick helper to resolve missing import
const AlertOctagon = AlertCircle;
