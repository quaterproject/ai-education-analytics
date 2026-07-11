import { Recommendation } from "./prediction";

export interface HumanReview {
  id: string;
  recommendation_id: string;
  status: 'PENDING_REVIEW' | 'APPROVED' | 'REJECTED' | 'MODIFIED';
  reviewed_by: string | null;
  educator_comment: string | null;
  rejection_reason: string | null;
  original_recommendation: Record<string, any>;
  modified_recommendation: Record<string, any> | null;
  reviewed_at: string | null;
  created_at: string;
}

export interface HumanReviewQueueItem extends HumanReview {
  recommendation: Recommendation | null;
  student_name: string | null;
  student_code: string | null;
  student_id: string | null;
  risk_level: 'LOW_RISK' | 'MEDIUM_RISK' | 'HIGH_RISK' | null;
  confidence: number | null;
}
