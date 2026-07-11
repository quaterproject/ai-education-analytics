import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Plus, Users } from 'lucide-react';
import { PageContainer } from '../components/layout/PageContainer';
import { StudentTable } from '../components/students/StudentTable';
import { StudentForm } from '../components/students/StudentForm';
import { getStudents, createStudent } from '../api/students';

export const StudentsPage: React.FC = () => {
  const queryClient = useQueryClient();
  const [showAddForm, setShowAddForm] = useState(false);

  // Fetch student registry
  const { data: students = [], isLoading } = useQuery({
    queryKey: ['students-registry'],
    queryFn: getStudents
  });

  // Register student mutation
  const createMutation = useMutation({
    mutationFn: createStudent,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['students-registry'] });
      setShowAddForm(false);
    }
  });

  if (isLoading) {
    return (
      <PageContainer>
        <div className="flex justify-between items-center pb-2 border-b border-slate-100">
          <div className="h-8 w-48 bg-slate-100 animate-pulse rounded" />
          <div className="h-10 w-32 bg-slate-100 animate-pulse rounded" />
        </div>
        <div className="h-96 bg-slate-100 animate-pulse rounded-2xl" />
      </PageContainer>
    );
  }

  // Map students to include mock/latest risk values for preview
  const extendedStudents = students.map(s => ({
    ...s,
    // Provide illustrative flags for dashboard presentation matching seed
    latest_risk: s.student_code === 'GP-001' || s.student_code === 'MS-002' ? 'HIGH_RISK' : (s.student_code === 'MS-001' ? 'MEDIUM_RISK' : 'LOW_RISK') as any,
    confidence: s.student_code === 'GP-001' ? 0.91 : (s.student_code === 'MS-002' ? 0.88 : (s.student_code === 'MS-001' ? 0.65 : 0.95)),
    last_assessment: s.created_at,
    review_status: s.student_code === 'GP-001' ? 'APPROVED' : (s.student_code === 'MS-002' ? 'REJECTED' : (s.student_code === 'MS-001' ? 'PENDING_REVIEW' : 'APPROVED')) as any
  }));

  return (
    <PageContainer>
      {/* Header action */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-2 border-b border-slate-100">
        <div className="flex items-center gap-3 text-slate-800">
          <Users className="h-6 w-6 text-blue-500" />
          <h2 className="text-xl font-bold tracking-tight">Student Registry</h2>
        </div>
        <button
          onClick={() => setShowAddForm(true)}
          className="inline-flex items-center gap-1.5 px-4 py-2.5 bg-blue-600 hover:bg-blue-700 text-white rounded-xl text-xs font-bold transition-all shadow-md shadow-blue-600/10"
        >
          <Plus className="h-4.5 w-4.5" />
          <span>Register Student</span>
        </button>
      </div>

      {/* Slide-over/Dialog Form overlay */}
      {showAddForm && (
        <div className="fixed inset-0 bg-slate-900/40 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <StudentForm
            onSubmit={(data) => createMutation.mutate(data)}
            onCancel={() => setShowAddForm(false)}
            isSubmitting={createMutation.isPending}
          />
        </div>
      )}

      {/* Registry Table */}
      <StudentTable students={extendedStudents} />
    </PageContainer>
  );
};
