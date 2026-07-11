export interface Student {
  id: string;
  student_code: string;
  first_name: string;
  last_name: string;
  age: number;
  gender: 'M' | 'F';
  school: 'GP' | 'MS';
  created_at: string;
  updated_at: string;
}

export interface AcademicRecord {
  id: string;
  student_id: string;
  study_time: number;
  failures: number;
  absences: number;
  family_support: 'yes' | 'no';
  school_support: 'yes' | 'no';
  internet_access: 'yes' | 'no';
  health: number;
  g1: number;
  g2: number;
  created_at: string;
}
