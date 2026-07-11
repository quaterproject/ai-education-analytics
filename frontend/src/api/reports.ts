import apiClient from './client';

export interface ReportResponse {
  report_id: string;
  file_type: 'pdf' | 'docx';
  filename: string;
  download_url: string;
  generated_at: string;
}

export const generatePdfReport = async (studentId: string): Promise<ReportResponse> => {
  const response = await apiClient.post<ReportResponse>(`/students/${studentId}/reports/pdf`);
  return response.data;
};

export const generateDocxReport = async (studentId: string): Promise<ReportResponse> => {
  const response = await apiClient.post<ReportResponse>(`/students/${studentId}/reports/docx`);
  return response.data;
};

export const getDownloadReportUrl = (reportId: string): string => {
  return `/api/v1/reports/${reportId}/download`;
};
