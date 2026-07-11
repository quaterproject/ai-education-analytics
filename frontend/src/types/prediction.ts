import { HumanReview } from "./review";

export interface Prediction {
  id: string;
  student_id: string;
  risk_level: 'LOW_RISK' | 'MEDIUM_RISK' | 'HIGH_RISK';
  confidence: number;
  class_probabilities: {
    LOW_RISK: number;
    MEDIUM_RISK: number;
    HIGH_RISK: number;
  };
  model_version: string;
  feature_values: Record<string, any>;
  shap_values: Record<string, number>;
  risk_factors: string[];
  protective_factors: string[];
  created_at: string;
  recommendation?: Recommendation | null;
}

export interface Recommendation {
  id: string;
  prediction_id: string;
  title: string;
  priority: 'LOW' | 'MEDIUM' | 'HIGH';
  summary: string;
  recommended_actions: string[];
  monitoring_plan: string[];
  success_indicators: string[];
  review_period_days: number;
  llm_model: string;
  created_at: string;
  review?: HumanReview | null;
}
