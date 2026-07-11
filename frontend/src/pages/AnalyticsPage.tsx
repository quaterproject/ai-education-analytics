import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { BarChart3, PieChart as PieIcon, LineChart as LineIcon, CheckCircle2, AlertTriangle, XCircle, Edit3 } from 'lucide-react';
import { PageContainer } from '../components/layout/PageContainer';
import { getOverview, getRiskDistribution, getInterventionStatus } from '../api/analytics';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, Legend, CartesianGrid, Cell } from 'recharts';
import { cn } from '../lib/utils';

export const AnalyticsPage: React.FC = () => {
  const { data: overview } = useQuery({
    queryKey: ['analytics-overview'],
    queryFn: getOverview
  });

  const { data: distribution = [] } = useQuery({
    queryKey: ['analytics-distribution'],
    queryFn: getRiskDistribution
  });

  const { data: status } = useQuery({
    queryKey: ['analytics-intervention-status'],
    queryFn: getInterventionStatus
  });

  // Data format for reviews chart
  const reviewChartData = [
    { name: 'Approved', count: status?.approved || 0, color: '#10B981' },
    { name: 'Modified', count: status?.modified || 0, color: '#F59E0B' },
    { name: 'Rejected', count: status?.rejected || 0, color: '#EF4444' },
    { name: 'Pending', count: status?.pending || 0, color: '#8B5CF6' }
  ];

  return (
    <PageContainer>
      <div className="flex items-center gap-3 pb-2 border-b border-slate-100">
        <BarChart3 className="h-6 w-6 text-blue-500" />
        <h2 className="text-xl font-bold tracking-tight">System Performance & Analytics</h2>
      </div>

      {/* Ratios row */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-slate-800">
        {/* Approvals */}
        <div className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Advisor Approval Rate</span>
            <CheckCircle2 className="h-5 w-5 text-emerald-500" />
          </div>
          <h3 className="text-4xl font-extrabold text-slate-800 tracking-tight">
            {status?.approval_rate ? `${Math.round(status.approval_rate * 100)}%` : '0%'}
          </h3>
          <p className="text-[10px] text-slate-400 font-semibold leading-relaxed">
            Percentage of AI programs approved without structural alterations.
          </p>
        </div>

        {/* Modifications */}
        <div className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Plan Alteration Rate</span>
            <Edit3 className="h-5 w-5 text-amber-500" />
          </div>
          <h3 className="text-4xl font-extrabold text-slate-800 tracking-tight">
            {status?.modification_rate ? `${Math.round(status.modification_rate * 100)}%` : '0%'}
          </h3>
          <p className="text-[10px] text-slate-400 font-semibold leading-relaxed">
            Percentage of generated programs modified by academic advisors during review.
          </p>
        </div>

        {/* Total Audits */}
        <div className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Total Audited Reviews</span>
            <BarChart3 className="h-5 w-5 text-blue-500" />
          </div>
          <h3 className="text-4xl font-extrabold text-slate-800 tracking-tight">
            {status ? (status.approved + status.rejected + status.modified) : 0}
          </h3>
          <p className="text-[10px] text-slate-400 font-semibold leading-relaxed">
            Total number of predictions evaluated by educators.
          </p>
        </div>
      </div>

      {/* Chart blocks */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Review states bar chart */}
        <div className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm h-[380px] flex flex-col">
          <h3 className="font-bold text-slate-800 text-sm mb-4">Intervention Workflow Outcomes</h3>
          <div className="flex-1 min-h-0">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={reviewChartData} margin={{ top: 10, right: 10, left: -25, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#F1F5F9" vertical={false} />
                <XAxis dataKey="name" stroke="#94A3B8" fontSize={11} tickLine={false} />
                <YAxis stroke="#94A3B8" fontSize={11} tickLine={false} allowDecimals={false} />
                <Tooltip cursor={{ fill: '#F8FAFC' }} />
                <Bar dataKey="count" radius={[6, 6, 0, 0]}>
                  {reviewChartData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Cohort risk profile breakdown */}
        <div className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm h-[380px] flex flex-col">
          <h3 className="font-bold text-slate-800 text-sm mb-4">Risk Class Cohort Breakdown</h3>
          <div className="flex-1 overflow-y-auto">
            <div className="space-y-4">
              {distribution.map((item) => {
                const colors = item.risk_level === 'HIGH_RISK' ? 'bg-red-500' : (item.risk_level === 'MEDIUM_RISK' ? 'bg-amber-500' : 'bg-emerald-500');
                const textColors = item.risk_level === 'HIGH_RISK' ? 'text-red-700' : (item.risk_level === 'MEDIUM_RISK' ? 'text-amber-700' : 'text-emerald-700');
                const bgs = item.risk_level === 'HIGH_RISK' ? 'bg-red-50' : (item.risk_level === 'MEDIUM_RISK' ? 'bg-amber-50' : 'bg-emerald-50');

                return (
                  <div key={item.risk_level} className="space-y-2">
                    <div className="flex items-center justify-between text-xs font-bold text-slate-700 uppercase">
                      <span>{item.risk_level.replace('_', ' ')}</span>
                      <span className={cn("px-2 py-0.5 rounded text-[10px]", bgs, textColors)}>{item.count} Students ({item.percentage}%)</span>
                    </div>
                    {/* Progress Bar */}
                    <div className="w-full bg-slate-100 h-2.5 rounded-full overflow-hidden">
                      <div className={cn("h-full transition-all duration-500", colors)} style={{ width: `${item.percentage}%` }} />
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </div>
    </PageContainer>
  );
};
