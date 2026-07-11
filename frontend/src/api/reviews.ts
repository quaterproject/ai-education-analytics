import apiClient from './client';
import { HumanReview, HumanReviewQueueItem } from '../types/review';

export const getPendingReviews = async (): Promise<HumanReviewQueueItem[]> => {
  const response = await apiClient.get<HumanReviewQueueItem[]>('/reviews/pending');
  return response.data;
};

export const approveRecommendation = async (
  recommendationId: string,
  reviewedBy: string,
  educatorComment?: string
): Promise<HumanReview> => {
  const response = await apiClient.post<HumanReview>(`/recommendations/${recommendationId}/approve`, {
    reviewed_by: reviewedBy,
    educator_comment: educatorComment || null
  });
  return response.data;
};

export const rejectRecommendation = async (
  recommendationId: string,
  reviewedBy: string,
  rejectionReason: string
): Promise<HumanReview> => {
  const response = await apiClient.post<HumanReview>(`/recommendations/${recommendationId}/reject`, {
    reviewed_by: reviewedBy,
    rejection_reason: rejectionReason
  });
  return response.data;
};

export const modifyRecommendation = async (
  recommendationId: string,
  reviewedBy: string,
  educatorComment: string,
  modifiedRecommendation: {
    title: string;
    priority: string;
    summary: string;
    recommended_actions: string[];
    monitoring_plan: string[];
    success_indicators: string[];
    review_period_days: number;
  }
): Promise<HumanReview> => {
  const response = await apiClient.post<HumanReview>(`/recommendations/${recommendationId}/modify`, {
    reviewed_by: reviewedBy,
    educator_comment: educatorComment || null,
    modified_recommendation: modifiedRecommendation
  });
  return response.data;
};
