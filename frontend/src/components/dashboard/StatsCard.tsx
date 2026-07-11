import React from 'react';
import { LucideIcon } from 'lucide-react';
import { cn } from '../../lib/utils';

interface StatsCardProps {
  title: string;
  value: string | number;
  icon: LucideIcon;
  description?: string;
  iconClassName?: string;
  className?: string;
}

export const StatsCard: React.FC<StatsCardProps> = ({
  title,
  value,
  icon: Icon,
  description,
  iconClassName,
  className
}) => {
  return (
    <div className={cn(
      "bg-white p-6 rounded-2xl border border-slate-100 shadow-sm transition-all duration-300 hover:shadow-md hover:-translate-y-0.5 flex items-start justify-between group",
      className
    )}>
      <div className="space-y-2">
        <span className="text-sm font-semibold text-slate-500 tracking-wide">{title}</span>
        <h3 className="text-3xl font-bold text-slate-800 tracking-tight">{value}</h3>
        {description && (
          <p className="text-xs text-slate-400 font-medium">{description}</p>
        )}
      </div>
      <div className={cn(
        "p-3 rounded-xl bg-slate-50 transition-colors duration-300 group-hover:bg-slate-100",
        iconClassName
      )}>
        <Icon className="h-6 w-6" />
      </div>
    </div>
  );
};
