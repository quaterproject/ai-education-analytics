import apiClient from './client';
import { Document } from '../types/document';

export const uploadDocument = async (studentId: string, file: File): Promise<Document> => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await apiClient.post<Document>(`/students/${studentId}/documents`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export const listStudentDocuments = async (studentId: string): Promise<Document[]> => {
  const response = await apiClient.get<Document[]>(`/students/${studentId}/documents`);
  return response.data;
};

export const getDocument = async (documentId: string): Promise<Document> => {
  const response = await apiClient.get<Document>(`/documents/${documentId}`);
  return response.data;
};
