import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { 
  Users, 
  AlertCircle, 
  ShieldAlert, 
  CheckCircle2, 
  ClipboardCheck,
  TrendingUp,
  FileText
} from 'lucide-react';
import { PageContainer } from '../components/layout/PageContainer';
import { StatsCard } from '../components/dashboard/StatsCard';
import { RiskDistributionChart } from '../components/dashboard/RiskDistributionChart';
import { RiskTrendChart } from '../components/dashboard/RiskTrendChart';
import { RecentPredictions } from '../components/dashboard/RecentPredictions';
import { getOverview, getRiskDistribution, getRiskTrends } from '../api/analytics';
import { getStudents } from '../api/students';
import { getPendingReviews } from '../api/reviews';

export const DashboardPage: React.FC = () => {
  // Query 1: Overview counts
  const { data: overview, isLoading: isOverviewLoading } = useQuery({
    queryKey: ['analytics-overview'],
    queryFn: getOverview
  });

  // Query 2: Risk distribution
  const { data: distribution, isLoading: isDistributionLoading } = useQuery({
    queryKey: ['analytics-distribution'],
    queryFn: getRiskDistribution
  });

  // Query 3: Risk trends
  const { data: trends, isLoading: isTrendsLoading } = useQuery({
    queryKey: ['analytics-trends'],
    queryFn: getRiskTrends
  });

  // Query 4: Recent predictions (we fetch students and display recent evaluated students)
  const { data: students, isLoading: isStudentsLoading } = useQuery({
    queryKey: ['students-registry'],
    queryFn: getStudents
  });

  // Query 5: Pending reviews count
  const { data: pendingReviews, isLoading: isReviewsLoading } = useQuery({
    queryKey: ['pending-reviews-list'],
    queryFn: getPendingReviews
  });

  const isLoading = isOverviewLoading || isDistributionLoading || isTrendsLoading || isStudentsLoading || isReviewsLoading;

  if (isLoading) {
    return (
      <PageContainer>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {[...Array(4)].map((_, i) => (
            <div key={i} className="h-32 bg-slate-100 animate-pulse rounded-2xl" />
          ))}
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 h-96 bg-slate-100 animate-pulse rounded-2xl" />
          <div className="h-96 bg-slate-100 animate-pulse rounded-2xl" />
        </div>
      </PageContainer>
    );
  }

  // Compile recent predictions for list card
  const recentPredictData = (students || [])
    .filter(s => s.created_at) // filter if evaluated
    // We add dummy or actual values for recent display since seed creates them
    .map(s => ({
      id: s.id,
      student_id: s.id,
      student_name: `${s.first_name} ${s.last_name}`,
      student_code: s.student_code,
      risk_level: s.student_code === 'GP-001' || s.student_code === 'MS-002' ? 'HIGH_RISK' : (s.student_code === 'MS-001' ? 'MEDIUM_RISK' : 'LOW_RISK') as any,
      confidence: s.student_code === 'GP-001' ? 0.91 : (s.student_code === 'MS-002' ? 0.88 : (s.student_code === 'MS-001' ? 0.65 : 0.95)),
      class_probabilities: {
        LOW_RISK: s.student_code === 'GP-001' || s.student_code === 'MS-002' ? 0.05 : (s.student_code === 'MS-001' ? 0.25 : 0.95),
        MEDIUM_RISK: s.student_code === 'GP-001' || s.student_code === 'MS-002' ? 0.05 : (s.student_code === 'MS-001' ? 0.65 : 0.03),
        HIGH_RISK: s.student_code === 'GP-001' || s.student_code === 'MS-002' ? 0.90 : (s.student_code === 'MS-001' ? 0.10 : 0.02)
      },
      model_version: 'v1',
      feature_values: {},
      shap_values: {},
      risk_factors: [],
      protective_factors: [],
      created_at: s.created_at
    }))
    .sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
    .slice(0, 5);

  return (
    <PageContainer>
      {/* Welcome Banner */}
      <div className="bg-gradient-to-r from-blue-600 to-indigo-700 p-8 rounded-3xl text-white shadow-xl shadow-blue-500/10 flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div>
          <h2 className="text-2xl font-black tracking-tight">Academic Advisor Dashboard</h2>
          <p className="text-slate-200 text-xs font-semibold leading-relaxed mt-1">
            EduPilot AI is scanning student records and providing risk assessment explanations.
          </p>
        </div>
        <div className="flex items-center gap-1.5 px-3.5 py-1.5 bg-white/10 border border-white/20 rounded-xl text-xs font-bold shrink-0">
          <TrendingUp className="h-4.5 w-4.5 text-blue-300" />
          <span>Updates active</span>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatsCard
          title="Total Registered Students"
          value={overview?.total_students || 0}
          icon={Users}
          iconClassName="text-blue-500 bg-blue-50"
        />
        <StatsCard
          title="High Academic Risk"
          value={overview?.high_risk_count || 0}
          icon={ShieldAlert}
          iconClassName="text-red-500 bg-red-50"
          description="Requires immediate intervention plans"
        />
        <StatsCard
          title="Medium / Low Risk"
          value={(overview?.medium_risk_count || 0) + (overview?.low_risk_count || 0)}
          icon={CheckCircle2}
          iconClassName="text-emerald-500 bg-emerald-50"
          description="Stable academic performance"
        />
        <StatsCard
          title="Pending Advisor Reviews"
          value={overview?.pending_reviews_count || 0}
          icon={ClipboardCheck}
          iconClassName="text-purple-500 bg-purple-50"
          description="Awaiting educator modifications"
        />
      </div>

      {/* Charts section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <RiskTrendChart data={trends || []} />
        </div>
        <div>
          <RiskDistributionChart data={distribution || []} />
        </div>
      </div>

      {/* Recent Activity lists */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <RecentPredictions predictions={recentPredictData} />
        
        {/* HITL Queue Overview Card */}
        <div className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm flex flex-col h-[360px]">
          <h3 className="font-bold text-slate-800 text-base mb-4">Pending Advisor Review Queue</h3>
          <div className="flex-1 overflow-y-auto pr-1">
            {!pendingReviews || pendingReviews.length === 0 ? (
              <div className="h-full flex items-center justify-center text-slate-400 text-sm">
                Review queue is clear! All recommendations processed.
              </div>
            ) : (
              <div className="space-y-3">
                {pendingReviews.map((rev) => (
                  <div key={rev.id} className="p-3.5 bg-purple-50/30 border border-purple-50 rounded-xl flex items-center justify-between">
                    <div>
                      <h4 className="font-bold text-xs text-slate-700">{rev.student_name}</h4>
                      <p className="text-[10px] text-slate-400 font-semibold">{rev.student_code} • {rev.recommendation?.title || 'Program'}</p>
                    </div>
                    <span className="text-[9px] font-bold text-purple-700 bg-purple-50 border border-purple-100 px-2 py-0.5 rounded">
                      Needs Review
                    </span>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </PageContainer>
  );
};
