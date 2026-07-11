import React, { useState } from 'react';
import { Check, X, Edit, Eye, ShieldAlert, Sparkles, UserCheck } from 'lucide-react';
import { Recommendation } from '../../types/prediction';
import { HumanReview } from '../../types/review';
import { cn } from '../../lib/utils';

interface HumanReviewPanelProps {
  recommendation: Recommendation;
  review: HumanReview;
  onApprove: (reviewedBy: string, comment?: string) => Promise<void>;
  onReject: (reviewedBy: string, reason: string) => Promise<void>;
  onModify: (reviewedBy: string, comment: string, modifiedData: any) => Promise<void>;
  isSubmitting?: boolean;
}

export const HumanReviewPanel: React.FC<HumanReviewPanelProps> = ({
  recommendation,
  review,
  onApprove,
  onReject,
  onModify,
  isSubmitting = false
}) => {
  const [activeForm, setActiveForm] = useState<'NONE' | 'APPROVE' | 'REJECT' | 'MODIFY'>('NONE');
  const [reviewerName, setReviewerName] = useState('Seymour Skinner');
  const [comment, setComment] = useState('');
  const [rejectionReason, setRejectionReason] = useState('');

  // Modify form state fields
  const [modTitle, setModTitle] = useState(recommendation.title);
  const [modPriority, setModPriority] = useState(recommendation.priority);
  const [modSummary, setModSummary] = useState(recommendation.summary);
  const [modPeriod, setModPeriod] = useState(recommendation.review_period_days);
  const [modActions, setModActions] = useState(recommendation.recommended_actions.join('\n'));
  const [modMonitor, setModMonitor] = useState(recommendation.monitoring_plan.join('\n'));
  const [modSuccess, setModSuccess] = useState(recommendation.success_indicators.join('\n'));

  const handleApprove = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!reviewerName.trim()) return;
    await onApprove(reviewerName, comment);
    setActiveForm('NONE');
  };

  const handleReject = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!reviewerName.trim() || !rejectionReason.trim()) return;
    await onReject(reviewerName, rejectionReason);
    setActiveForm('NONE');
  };

  const handleModify = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!reviewerName.trim()) return;
    
    const modifiedPayload = {
      title: modTitle.trim(),
      priority: modPriority,
      summary: modSummary.trim(),
      recommended_actions: modActions.split('\n').map(a => a.trim()).filter(Boolean),
      monitoring_plan: modMonitor.split('\n').map(m => m.trim()).filter(Boolean),
      success_indicators: modSuccess.split('\n').map(s => s.trim()).filter(Boolean),
      review_period_days: Number(modPeriod)
    };

    await onModify(reviewerName, comment, modifiedPayload);
    setActiveForm('NONE');
  };

  const renderActiveReviewState = () => {
    if (review.status === 'PENDING_REVIEW') {
      return (
        <div className="flex flex-col space-y-4">
          <div className="flex flex-wrap items-center gap-3">
            <button
              onClick={() => { setActiveForm('APPROVE'); setComment(''); }}
              className="px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl text-xs font-bold flex items-center gap-1.5 transition-colors shadow-md shadow-emerald-600/10"
              disabled={isSubmitting}
            >
              <Check className="h-4.5 w-4.5" />
              <span>Approve Program</span>
            </button>
            <button
              onClick={() => { setActiveForm('MODIFY'); setComment(''); }}
              className="px-4 py-2 bg-amber-500 hover:bg-amber-600 text-white rounded-xl text-xs font-bold flex items-center gap-1.5 transition-colors shadow-md shadow-amber-500/10"
              disabled={isSubmitting}
            >
              <Edit className="h-4.5 w-4.5" />
              <span>Modify Recommendations</span>
            </button>
            <button
              onClick={() => { setActiveForm('REJECT'); setRejectionReason(''); }}
              className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-xl text-xs font-bold flex items-center gap-1.5 transition-colors shadow-md shadow-red-600/10"
              disabled={isSubmitting}
            >
              <X className="h-4.5 w-4.5" />
              <span>Reject Program</span>
            </button>
          </div>

          {/* Form renders */}
          {activeForm === 'APPROVE' && (
            <form onSubmit={handleApprove} className="p-5 bg-emerald-50/30 border border-emerald-100 rounded-2xl space-y-4">
              <h5 className="text-xs font-extrabold text-emerald-800 uppercase tracking-wide">Approve Recommendation</h5>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                <div>
                  <label className="block text-slate-500 font-bold mb-1">Reviewed By (Educator Name)</label>
                  <input
                    type="text"
                    className="w-full px-3 py-2 border border-slate-200 rounded-lg focus:outline-none focus:ring-1 focus:ring-blue-500 bg-white"
                    value={reviewerName}
                    onChange={(e) => setReviewerName(e.target.value)}
                    required
                  />
                </div>
                <div>
                  <label className="block text-slate-500 font-bold mb-1">Educator Comment (Optional)</label>
                  <input
                    type="text"
                    placeholder="Provide comments or additional context..."
                    className="w-full px-3 py-2 border border-slate-200 rounded-lg focus:outline-none focus:ring-1 focus:ring-blue-500 bg-white"
                    value={comment}
                    onChange={(e) => setComment(e.target.value)}
                  />
                </div>
              </div>
              <div className="flex justify-end gap-2 text-xs">
                <button
                  type="button"
                  onClick={() => setActiveForm('NONE')}
                  className="px-3.5 py-1.5 border border-slate-200 text-slate-500 rounded-lg font-bold hover:bg-slate-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-1.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg font-bold"
                  disabled={isSubmitting}
                >
                  Confirm Approval
                </button>
              </div>
            </form>
          )}

          {activeForm === 'REJECT' && (
            <form onSubmit={handleReject} className="p-5 bg-red-50/20 border border-red-100 rounded-2xl space-y-4">
              <h5 className="text-xs font-extrabold text-red-800 uppercase tracking-wide">Reject Recommendation</h5>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                <div>
                  <label className="block text-slate-500 font-bold mb-1">Reviewed By</label>
                  <input
                    type="text"
                    className="w-full px-3 py-2 border border-slate-200 rounded-lg focus:outline-none focus:ring-1 focus:ring-blue-500 bg-white"
                    value={reviewerName}
                    onChange={(e) => setReviewerName(e.target.value)}
                    required
                  />
                </div>
                <div>
                  <label className="block text-slate-500 font-bold mb-1">Reason for Rejection</label>
                  <input
                    type="text"
                    placeholder="Why are you rejecting this recommendation?"
                    className="w-full px-3 py-2 border border-slate-200 rounded-lg focus:outline-none focus:ring-1 focus:ring-blue-500 bg-white"
                    value={rejectionReason}
                    onChange={(e) => setRejectionReason(e.target.value)}
                    required
                  />
                </div>
              </div>
              <div className="flex justify-end gap-2 text-xs">
                <button
                  type="button"
                  onClick={() => setActiveForm('NONE')}
                  className="px-3.5 py-1.5 border border-slate-200 text-slate-500 rounded-lg font-bold hover:bg-slate-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-1.5 bg-red-600 hover:bg-red-700 text-white rounded-lg font-bold"
                  disabled={isSubmitting}
                >
                  Confirm Rejection
                </button>
              </div>
            </form>
          )}

          {activeForm === 'MODIFY' && (
            <form onSubmit={handleModify} className="p-5 bg-amber-50/20 border border-amber-100 rounded-2xl space-y-4">
              <h5 className="text-xs font-extrabold text-amber-800 uppercase tracking-wide">Modify Recommendation Details</h5>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
                {/* Reviewer Name */}
                <div>
                  <label className="block text-slate-500 font-bold mb-1">Reviewed By</label>
                  <input
                    type="text"
                    className="w-full px-3 py-2 border border-slate-200 rounded-lg focus:outline-none bg-white font-semibold"
                    value={reviewerName}
                    onChange={(e) => setReviewerName(e.target.value)}
                    required
                  />
                </div>
                
                {/* Title */}
                <div className="col-span-2">
                  <label className="block text-slate-500 font-bold mb-1">Intervention Title</label>
                  <input
                    type="text"
                    className="w-full px-3 py-2 border border-slate-200 rounded-lg focus:outline-none bg-white font-semibold"
                    value={modTitle}
                    onChange={(e) => setModTitle(e.target.value)}
                    required
                  />
                </div>

                {/* Priority */}
                <div>
                  <label className="block text-slate-500 font-bold mb-1">Priority</label>
                  <select
                    className="w-full px-3 py-2 border border-slate-200 rounded-lg focus:outline-none bg-white font-semibold"
                    value={modPriority}
                    onChange={(e) => setModPriority(e.target.value as any)}
                  >
                    <option value="LOW">LOW</option>
                    <option value="MEDIUM">MEDIUM</option>
                    <option value="HIGH">HIGH</option>
                  </select>
                </div>

                {/* Review Period */}
                <div>
                  <label className="block text-slate-500 font-bold mb-1">Review Period (Days)</label>
                  <input
                    type="number"
                    className="w-full px-3 py-2 border border-slate-200 rounded-lg focus:outline-none bg-white font-semibold"
                    value={modPeriod}
                    onChange={(e) => setModPeriod(Number(e.target.value))}
                    required
                  />
                </div>

                {/* Comment */}
                <div>
                  <label className="block text-slate-500 font-bold mb-1">Modification Comments</label>
                  <input
                    type="text"
                    placeholder="Explain the changes made..."
                    className="w-full px-3 py-2 border border-slate-200 rounded-lg focus:outline-none bg-white font-semibold"
                    value={comment}
                    onChange={(e) => setComment(e.target.value)}
                    required
                  />
                </div>

                {/* Summary */}
                <div className="col-span-3">
                  <label className="block text-slate-500 font-bold mb-1">Intervention Summary</label>
                  <textarea
                    className="w-full px-3 py-2 border border-slate-200 rounded-lg focus:outline-none bg-white text-xs font-semibold leading-relaxed"
                    rows={2}
                    value={modSummary}
                    onChange={(e) => setModSummary(e.target.value)}
                    required
                  />
                </div>

                {/* Actions (list block split by newline) */}
                <div>
                  <label className="block text-slate-500 font-bold mb-1">Action Steps (One per line)</label>
                  <textarea
                    className="w-full px-3 py-2 border border-slate-200 rounded-lg focus:outline-none bg-white text-xs font-mono"
                    rows={4}
                    value={modActions}
                    onChange={(e) => setModActions(e.target.value)}
                    required
                  />
                </div>

                {/* Monitor (list block split by newline) */}
                <div>
                  <label className="block text-slate-500 font-bold mb-1">Monitoring (One per line)</label>
                  <textarea
                    className="w-full px-3 py-2 border border-slate-200 rounded-lg focus:outline-none bg-white text-xs font-mono"
                    rows={4}
                    value={modMonitor}
                    onChange={(e) => setModMonitor(e.target.value)}
                    required
                  />
                </div>

                {/* Success (list block split by newline) */}
                <div>
                  <label className="block text-slate-500 font-bold mb-1">Success Indicators (One per line)</label>
                  <textarea
                    className="w-full px-3 py-2 border border-slate-200 rounded-lg focus:outline-none bg-white text-xs font-mono"
                    rows={4}
                    value={modSuccess}
                    onChange={(e) => setModSuccess(e.target.value)}
                    required
                  />
                </div>
              </div>

              <div className="flex justify-end gap-2 text-xs pt-3 border-t border-slate-100">
                <button
                  type="button"
                  onClick={() => setActiveForm('NONE')}
                  className="px-3.5 py-1.5 border border-slate-200 text-slate-500 rounded-lg font-bold hover:bg-slate-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-1.5 bg-amber-500 hover:bg-amber-600 text-white rounded-lg font-bold"
                  disabled={isSubmitting}
                >
                  Save Modifications
                </button>
              </div>
            </form>
          )}
        </div>
      );
    }

    // Handled/Reviewed States
    return (
      <div className="p-5 rounded-2xl border bg-slate-50 text-xs space-y-4">
        {/* Header indicator */}
        <div className="flex items-center gap-2">
          <UserCheck className="h-5 w-5 text-blue-500" />
          <h4 className="font-bold text-slate-800 text-sm">Educator Audit Log</h4>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 font-semibold text-slate-600">
          <div>
            <span className="text-[10px] text-slate-400 uppercase block mb-1">Educator Decision</span>
            <span className={cn(
              "px-2 py-0.5 border text-[10px] font-bold rounded",
              review.status === 'APPROVED' ? 'bg-emerald-50 border-emerald-100 text-emerald-700' :
              (review.status === 'REJECTED' ? 'bg-red-50 border-red-100 text-red-700' : 'bg-amber-50 border-amber-100 text-amber-700')
            )}>
              {review.status}
            </span>
          </div>

          <div>
            <span className="text-[10px] text-slate-400 uppercase block mb-1">Reviewed By</span>
            <p className="text-slate-800 font-bold">{review.reviewed_by}</p>
          </div>

          {review.reviewed_at && (
            <div>
              <span className="text-[10px] text-slate-400 uppercase block mb-1">Reviewed At</span>
              <p className="text-slate-800">{new Date(review.reviewed_at).toLocaleString()}</p>
            </div>
          )}

          {review.educator_comment && (
            <div className="col-span-2 border-t border-slate-200/60 pt-3">
              <span className="text-[10px] text-slate-400 uppercase block mb-1">Educator Review Comments</span>
              <p className="p-2.5 bg-slate-100 text-slate-700 rounded-xl leading-relaxed italic border border-slate-200/30">
                "{review.educator_comment}"
              </p>
            </div>
          )}

          {review.rejection_reason && (
            <div className="col-span-2 border-t border-slate-200/60 pt-3">
              <span className="text-[10px] text-slate-400 uppercase block mb-1">Rejection Explanation</span>
              <p className="p-2.5 bg-red-50 text-red-700 border border-red-100/50 rounded-xl leading-relaxed">
                {review.rejection_reason}
              </p>
            </div>
          )}
        </div>

        {/* Audit Diff: original side-by-side with modified */}
        {review.status === 'MODIFIED' && review.modified_recommendation && (
          <div className="border-t border-slate-200/60 pt-4 space-y-4">
            <h5 className="text-[10px] font-bold text-slate-500 uppercase tracking-wider">Side-by-Side Modification Comparison</h5>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {/* Original */}
              <div className="p-4 bg-slate-100 rounded-xl border border-slate-200 space-y-2">
                <span className="text-[9px] font-bold text-slate-400 uppercase block tracking-wider">Original AI Proposal</span>
                <h6 className="font-extrabold text-slate-700">{review.original_recommendation.title}</h6>
                <p className="text-[11px] text-slate-500 leading-relaxed italic">"{review.original_recommendation.summary}"</p>
                <div className="pt-2">
                  <span className="text-[9px] font-bold text-slate-400 uppercase block">Action Steps</span>
                  <ul className="list-disc pl-4 space-y-1 text-[11px] text-slate-600">
                    {review.original_recommendation.recommended_actions.map((act: string, idx: number) => (
                      <li key={idx}>{act}</li>
                    ))}
                  </ul>
                </div>
              </div>

              {/* Modified */}
              <div className="p-4 bg-amber-50/30 rounded-xl border border-amber-100/50 space-y-2">
                <span className="text-[9px] font-bold text-amber-600 uppercase block tracking-wider">Educator Approved Plan</span>
                <h6 className="font-extrabold text-slate-800">{review.modified_recommendation.title}</h6>
                <p className="text-[11px] text-slate-700 leading-relaxed font-medium">"{review.modified_recommendation.summary}"</p>
                <div className="pt-2">
                  <span className="text-[9px] font-bold text-slate-400 uppercase block">Action Steps</span>
                  <ul className="list-disc pl-4 space-y-1 text-[11px] text-slate-700 font-medium">
                    {review.modified_recommendation.recommended_actions.map((act: string, idx: number) => (
                      <li key={idx}>{act}</li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm space-y-6">
      <div className="flex items-center gap-2 border-b border-slate-100 pb-3 text-slate-700">
        <Sparkles className="h-5 w-5 text-blue-500" />
        <h4 className="font-bold text-sm uppercase tracking-wide">Human-in-the-Loop Review Panel</h4>
      </div>

      {renderActiveReviewState()}
    </div>
  );
};
