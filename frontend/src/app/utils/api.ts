const BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface Assessment {
  id: number;
  asset_name: string;
  location: string;
  description?: string;
  created_at: string;
  sensor_csv_path?: string;
  image_path?: string;
  audio_path?: string;
  lstm_prediction_class: number;
  lstm_confidence_scores: number[];
  lstm_feature_importance: Record<string, number>;
  cnn_prediction_class: number;
  cnn_confidence_score: number;
  cnn_gradcam_path?: string;
  ann_prediction_class: number;
  ann_confidence_score: number;
  llm_summary?: string;
  llm_reasoning?: string;
  llm_mitigation?: string;
  is_reviewed: boolean;
  override_lstm_class?: number;
  override_cnn_class?: number;
  override_ann_class?: number;
  analyst_notes?: string;
  reviewed_by?: string;
  reviewed_at?: string;
}

export async function fetchAssessments(): Promise<Assessment[]> {
  const res = await fetch(`${BASE_URL}/api/assessments`);
  if (!res.ok) throw new Error('Failed to fetch assessments');
  return res.json();
}

export async function fetchAssessmentById(id: number): Promise<Assessment> {
  const res = await fetch(`${BASE_URL}/api/assessments/${id}`);
  if (!res.ok) throw new Error('Failed to fetch assessment detail');
  return res.json();
}

export async function createAssessment(formData: FormData): Promise<Assessment> {
  const res = await fetch(`${BASE_URL}/api/assessments`, {
    method: 'POST',
    body: formData,
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || 'Failed to submit inspection');
  }
  return res.json();
}

export async function submitHitlReview(
  id: number,
  data: {
    override_lstm_class?: number;
    override_cnn_class?: number;
    override_ann_class?: number;
    analyst_notes?: string;
    reviewed_by?: string;
  }
): Promise<Assessment> {
  const body = new FormData();
  if (data.override_lstm_class !== undefined && data.override_lstm_class !== null) {
    body.append('override_lstm_class', data.override_lstm_class.toString());
  }
  if (data.override_cnn_class !== undefined && data.override_cnn_class !== null) {
    body.append('override_cnn_class', data.override_cnn_class.toString());
  }
  if (data.override_ann_class !== undefined && data.override_ann_class !== null) {
    body.append('override_ann_class', data.override_ann_class.toString());
  }
  if (data.analyst_notes) {
    body.append('analyst_notes', data.analyst_notes);
  }
  if (data.reviewed_by) {
    body.append('reviewed_by', data.reviewed_by);
  }

  const res = await fetch(`${BASE_URL}/api/assessments/${id}/hitl`, {
    method: 'POST',
    body,
  });
  if (!res.ok) throw new Error('Failed to submit HITL review');
  return res.json();
}

export function getPdfDownloadUrl(id: number): string {
  return `${BASE_URL}/api/assessments/${id}/pdf`;
}

export function getStaticFileUrl(path?: string): string {
  if (!path) return '';
  // Normalize windows paths to slashes and prepend server base
  const cleanPath = path.replace(/\\/g, '/');
  return `${BASE_URL}/${cleanPath}`;
}
