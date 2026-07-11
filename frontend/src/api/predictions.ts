import apiClient from './client';
import { Prediction, Recommendation } from '../types/prediction';

export const predictStudentRisk = async (
  studentId: string,
  modelType: 'EARLY_WARNING' | 'LATE_STAGE' = 'LATE_STAGE'
): Promise<Prediction> => {
  const response = await apiClient.post<Prediction>(`/students/${studentId}/predict?model_type=${modelType}`);
  return response.data;
};

export const getStudentPredictions = async (studentId: string): Promise<Prediction[]> => {
  const response = await apiClient.get<Prediction[]>(`/students/${studentId}/predictions`);
  return response.data;
};

export const getPrediction = async (predictionId: string): Promise<Prediction> => {
  const response = await apiClient.get<Prediction>(`/predictions/${predictionId}`);
  return response.data;
};

export const generateRecommendation = async (
  predictionId: string,
  teacherNotes?: string,
  documentId?: string
): Promise<Recommendation> => {
  const response = await apiClient.post<Recommendation>(`/predictions/${predictionId}/recommendation`, {
    teacher_notes: teacherNotes || null,
    document_id: documentId || null
  });
  return response.data;
};

export const getRecommendation = async (recommendationId: string): Promise<Recommendation> => {
  const response = await apiClient.get<Recommendation>(`/recommendations/${recommendationId}`);
  return response.data;
};
