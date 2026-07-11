import React from 'react';
import { Bell, ShieldAlert, CheckCircle2 } from 'lucide-react';

interface HeaderProps {
  title: string;
}

export const Header: React.FC<HeaderProps> = ({ title }) => {
  return (
    <header className="h-20 border-b border-slate-200 bg-white flex items-center justify-between px-8 sticky top-0 z-30 shadow-sm">
      {/* Page Title */}
      <div>
        <h2 className="text-xl font-bold text-slate-800 tracking-tight">{title}</h2>
      </div>

      {/* Action panel & notifications */}
      <div className="flex items-center gap-6">
        {/* API connection status badge */}
        <div className="flex items-center gap-1.5 px-3 py-1 bg-emerald-50 border border-emerald-100 text-emerald-700 text-xs font-semibold rounded-full">
          <CheckCircle2 className="h-3.5 w-3.5" />
          <span>Core API Connected</span>
        </div>

        {/* Advisor details */}
        <div className="flex items-center gap-3 pl-4 border-l border-slate-200">
          <div className="text-right">
            <h4 className="text-sm font-semibold text-slate-700">Seymour Skinner</h4>
            <span className="text-xs text-slate-500 font-medium">Academic Advisor</span>
          </div>
          <div className="h-10 w-10 bg-slate-100 rounded-full border border-slate-200 flex items-center justify-center font-bold text-slate-700 shadow-inner">
            SS
          </div>
        </div>
      </div>
    </header>
  );
};
