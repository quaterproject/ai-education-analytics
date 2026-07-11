export interface Document {
  id: string;
  student_id: string;
  filename: string;
  file_type: 'pdf' | 'png' | 'jpg' | 'jpeg' | 'webp';
  file_path: string;
  processing_status: 'PENDING' | 'PROCESSING' | 'COMPLETED' | 'FAILED';
  extracted_text: string | null;
  structured_data: Record<string, any> | null;
  created_at: string;
}
