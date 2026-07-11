import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import { ClipboardCheck, Search, ShieldAlert, CheckCircle2, AlertTriangle, ArrowRight, UserCheck } from 'lucide-react';
import { PageContainer } from '../components/layout/PageContainer';
import { getPendingReviews, approveRecommendation, rejectRecommendation, modifyRecommendation } from '../api/reviews';
import { HumanReviewQueueItem } from '../types/review';
import { HumanReviewPanel } from '../components/reviews/HumanReviewPanel';
import { cn } from '../lib/utils';

export const ReviewQueuePage: React.FC = () => {
  const queryClient = useQueryClient();
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedReview, setSelectedReview] = useState<HumanReviewQueueItem | null>(null);

  // Fetch pending review queue
  const { data: pendingReviews = [], isLoading } = useQuery({
    queryKey: ['pending-reviews-list'],
    queryFn: getPendingReviews
  });

  // Action mutations
  const approveMutation = useMutation({
    mutationFn: (args: { recId: string; reviewer: string; comment?: string }) => 
      approveRecommendation(args.recId, args.reviewer, args.comment),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['pending-reviews-list'] });
      queryClient.invalidateQueries({ queryKey: ['analytics-overview'] });
      setSelectedReview(null);
    }
  });

  const rejectMutation = useMutation({
    mutationFn: (args: { recId: string; reviewer: string; reason: string }) => 
      rejectRecommendation(args.recId, args.reviewer, args.reason),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['pending-reviews-list'] });
      queryClient.invalidateQueries({ queryKey: ['analytics-overview'] });
      setSelectedReview(null);
    }
  });

  const modifyMutation = useMutation({
    mutationFn: (args: { recId: string; reviewer: string; comment: string; modified: any }) => 
      modifyRecommendation(args.recId, args.reviewer, args.comment, args.modified),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['pending-reviews-list'] });
      queryClient.invalidateQueries({ queryKey: ['analytics-overview'] });
      setSelectedReview(null);
    }
  });

  const handleApprove = async (reviewer: string, comment?: string) => {
    if (!selectedReview?.recommendation_id) return;
    await approveMutation.mutateAsync({
      recId: selectedReview.recommendation_id,
      reviewer,
      comment
    });
  };

  const handleReject = async (reviewer: string, reason: string) => {
    if (!selectedReview?.recommendation_id) return;
    await rejectMutation.mutateAsync({
      recId: selectedReview.recommendation_id,
      reviewer,
      reason
    });
  };

  const handleModify = async (reviewer: string, comment: string, modified: any) => {
    if (!selectedReview?.recommendation_id) return;
    await modifyMutation.mutateAsync({
      recId: selectedReview.recommendation_id,
      reviewer,
      comment,
      modified
    });
  };

  const filteredReviews = pendingReviews.filter(rev => {
    const name = rev.student_name?.toLowerCase() || '';
    const code = rev.student_code?.toLowerCase() || '';
    const title = rev.recommendation?.title?.toLowerCase() || '';
    return name.includes(searchTerm.toLowerCase()) || 
           code.includes(searchTerm.toLowerCase()) || 
           title.includes(searchTerm.toLowerCase());
  });

  const getRiskBadge = (level?: string | null) => {
    if (!level) return null;
    switch (level) {
      case 'HIGH_RISK':
        return (
          <span className="inline-flex items-center gap-1 px-2 py-0.5 bg-red-50 text-red-700 text-[10px] font-bold border border-red-100 rounded-full">
            <span>High Risk</span>
          </span>
        );
      case 'MEDIUM_RISK':
        return (
          <span className="inline-flex items-center gap-1 px-2 py-0.5 bg-amber-50 text-amber-700 text-[10px] font-bold border border-amber-100 rounded-full">
            <span>Medium Risk</span>
          </span>
        );
      default:
        return (
          <span className="inline-flex items-center gap-1 px-2 py-0.5 bg-emerald-50 text-emerald-700 text-[10px] font-bold border border-emerald-100 rounded-full">
            <span>Low Risk</span>
          </span>
        );
    }
  };

  const isActionPending = approveMutation.isPending || rejectMutation.isPending || modifyMutation.isPending;

  return (
    <PageContainer>
      <div className="flex items-center gap-3 pb-2 border-b border-slate-100">
        <ClipboardCheck className="h-6 w-6 text-blue-500" />
        <h2 className="text-xl font-bold tracking-tight">Educator Review Queue</h2>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left: Pending List */}
        <div className="lg:col-span-1 bg-white rounded-2xl border border-slate-100 shadow-sm flex flex-col h-[600px] overflow-hidden">
          <div className="p-4 border-b border-slate-100 bg-slate-50/50">
            <div className="relative">
              <Search className="absolute left-3 top-2.5 h-4 w-4 text-slate-400" />
              <input
                type="text"
                placeholder="Search queue..."
                className="w-full pl-9 pr-4 py-1.5 border border-slate-200 rounded-xl text-xs focus:outline-none focus:ring-1 focus:ring-blue-500 bg-white"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
          </div>

          <div className="flex-1 overflow-y-auto divide-y divide-slate-100">
            {isLoading ? (
              [...Array(3)].map((_, i) => (
                <div key={i} className="p-4 space-y-2 animate-pulse">
                  <div className="h-4 w-32 bg-slate-100 rounded" />
                  <div className="h-3 w-48 bg-slate-100 rounded" />
                </div>
              ))
            ) : filteredReviews.length === 0 ? (
              <div className="h-full flex items-center justify-center p-8 text-center text-slate-400 text-xs font-semibold">
                No items pending educator review.
              </div>
            ) : (
              filteredReviews.map((rev) => (
                <button
                  key={rev.id}
                  onClick={() => setSelectedReview(rev)}
                  className={cn(
                    "w-full text-left p-4 hover:bg-slate-50 transition-colors flex items-start justify-between gap-2 border-l-4",
                    selectedReview?.id === rev.id ? "bg-blue-50/20 border-l-blue-600 hover:bg-blue-50/20" : "border-l-transparent"
                  )}
                >
                  <div className="space-y-1">
                    <h4 className="font-bold text-xs text-slate-800">{rev.student_name}</h4>
                    <p className="text-[10px] text-slate-500 font-bold">{rev.student_code} • Priority: {rev.recommendation?.priority}</p>
                    <p className="text-[10px] text-slate-400 font-medium truncate max-w-[200px]">{rev.recommendation?.title}</p>
                  </div>
                  <div className="flex flex-col items-end gap-1.5 shrink-0">
                    {getRiskBadge(rev.risk_level)}
                    <span className="text-[9px] text-slate-400 font-bold">{new Date(rev.created_at).toLocaleDateString()}</span>
                  </div>
                </button>
              ))
            )}
          </div>
        </div>

        {/* Right: Selected Detail Actions Panel */}
        <div className="lg:col-span-2 space-y-6">
          {selectedReview && selectedReview.recommendation ? (
            <div className="space-y-6 animate-in fade-in duration-300">
              <div className="bg-gradient-to-r from-slate-900 to-indigo-950 p-6 rounded-2xl text-slate-100 border border-slate-800 flex items-center justify-between">
                <div>
                  <span className="text-[9px] font-bold text-blue-400 bg-blue-400/10 px-2 py-0.5 rounded border border-blue-400/20 uppercase">
                    Focused Review Workspace
                  </span>
                  <h3 className="text-lg font-black text-white mt-1.5 tracking-tight">{selectedReview.student_name}</h3>
                  <p className="text-xs text-slate-400 font-semibold">{selectedReview.student_code} • {selectedReview.risk_level?.replace('_', ' ')}</p>
                </div>
                <Link
                  to={`/students/${selectedReview.student_id || selectedReview.recommendation.prediction_id}`}
                  className="px-3.5 py-1.5 bg-white/10 border border-white/20 hover:bg-white/20 text-white rounded-xl text-xs font-bold transition-all"
                >
                  View Full Profile
                </Link>
              </div>

              {/* Review Panel with original recommendation & modify tools */}
              <HumanReviewPanel
                recommendation={selectedReview.recommendation}
                review={selectedReview}
                onApprove={handleApprove}
                onReject={handleReject}
                onModify={handleModify}
                isSubmitting={isActionPending}
              />
            </div>
          ) : (
            <div className="bg-slate-50 border border-slate-200 rounded-2xl p-12 text-center text-slate-400 text-xs font-semibold h-[400px] flex flex-col items-center justify-center space-y-3">
              <UserCheck className="h-8 w-8 text-slate-300" />
              <div>
                <h4 className="font-bold text-slate-700 text-sm">Review Workspace Idle</h4>
                <p className="text-[10px] text-slate-400 font-semibold mt-1">Select a pending item from the left queue to open details.</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </PageContainer>
  );
};
