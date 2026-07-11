import apiClient from './client';

export interface OverviewStats {
  total_students: number;
  high_risk_count: number;
  medium_risk_count: number;
  low_risk_count: number;
  pending_reviews_count: number;
}

export interface RiskDistributionItem {
  risk_level: string;
  count: number;
  percentage: number;
}

export interface RiskTrendItem {
  date: string;
  high_risk: number;
  medium_risk: number;
  low_risk: number;
}

export interface InterventionStatusStats {
  pending: number;
  approved: number;
  rejected: number;
  modified: number;
  approval_rate: number;
  modification_rate: number;
}

export const getOverview = async (): Promise<OverviewStats> => {
  const response = await apiClient.get<OverviewStats>('/analytics/overview');
  return response.data;
};

export const getRiskDistribution = async (): Promise<RiskDistributionItem[]> => {
  const response = await apiClient.get<RiskDistributionItem[]>('/analytics/risk-distribution');
  return response.data;
};

export const getRiskTrends = async (): Promise<RiskTrendItem[]> => {
  const response = await apiClient.get<RiskTrendItem[]>('/analytics/risk-trends');
  return response.data;
};

export const getInterventionStatus = async (): Promise<InterventionStatusStats> => {
  const response = await apiClient.get<InterventionStatusStats>('/analytics/intervention-status');
  return response.data;
};
