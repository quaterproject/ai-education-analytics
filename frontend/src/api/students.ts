import apiClient from './client';
import { Student, AcademicRecord } from '../types/student';

export const getStudents = async (): Promise<Student[]> => {
  const response = await apiClient.get<Student[]>('/students');
  return response.data;
};

export const getStudent = async (id: string): Promise<Student> => {
  const response = await apiClient.get<Student>(`/students/${id}`);
  return response.data;
};

export const createStudent = async (student: Omit<Student, 'id' | 'created_at' | 'updated_at'>): Promise<Student> => {
  const response = await apiClient.post<Student>('/students', student);
  return response.data;
};

export const updateStudent = async (id: string, student: Partial<Student>): Promise<Student> => {
  const response = await apiClient.put<Student>(`/students/${id}`, student);
  return response.data;
};

export const deleteStudent = async (id: string): Promise<void> => {
  await apiClient.delete(`/students/${id}`);
};

export const addAcademicRecord = async (studentId: string, record: Omit<AcademicRecord, 'id' | 'student_id' | 'created_at'>): Promise<AcademicRecord> => {
  const response = await apiClient.post<AcademicRecord>(`/students/${studentId}/records`, record);
  return response.data;
};

export const getAcademicRecords = async (studentId: string): Promise<AcademicRecord[]> => {
  const response = await apiClient.get<AcademicRecord[]>(`/students/${studentId}/records`);
  return response.data;
};
