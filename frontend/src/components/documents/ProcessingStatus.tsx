import React from 'react';
import { Loader2, CheckCircle2, Circle, AlertCircle } from 'lucide-react';
import { cn } from '../../lib/utils';

export interface StepStatus {
  id: string;
  label: string;
  status: 'PENDING' | 'RUNNING' | 'COMPLETED' | 'FAILED';
}

interface ProcessingStatusProps {
  steps: StepStatus[];
}

export const ProcessingStatus: React.FC<ProcessingStatusProps> = ({ steps }) => {
  return (
    <div className="bg-slate-50 p-6 rounded-2xl border border-slate-200/60 space-y-4 max-w-md w-full">
      <h4 className="text-sm font-bold text-slate-700 uppercase tracking-wider pb-2 border-b border-slate-200">
        AI Pipeline Activity
      </h4>
      <div className="space-y-3.5">
        {steps.map((step) => {
          return (
            <div 
              key={step.id} 
              className={cn(
                "flex items-center justify-between text-xs font-semibold p-2.5 rounded-xl border transition-all duration-300",
                step.status === 'RUNNING' 
                  ? "bg-blue-50/50 border-blue-100 text-blue-700 shadow-sm" 
                  : (step.status === 'COMPLETED' 
                    ? "bg-emerald-50/20 border-emerald-50 text-slate-600" 
                    : (step.status === 'FAILED' 
                      ? "bg-red-50 border-red-100 text-red-700" 
                      : "bg-transparent border-transparent text-slate-400"))
              )}
            >
              <div className="flex items-center gap-2.5">
                {step.status === 'RUNNING' && (
                  <Loader2 className="h-4.5 w-4.5 text-blue-500 animate-spin" />
                )}
                {step.status === 'COMPLETED' && (
                  <CheckCircle2 className="h-4.5 w-4.5 text-emerald-500" />
                )}
                {step.status === 'FAILED' && (
                  <AlertCircle className="h-4.5 w-4.5 text-red-500" />
                )}
                {step.status === 'PENDING' && (
                  <Circle className="h-4.5 w-4.5 text-slate-300" />
                )}
                <span>{step.label}</span>
              </div>
              <span className="text-[10px] uppercase font-bold tracking-wider opacity-75">
                {step.status.toLowerCase()}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
};
