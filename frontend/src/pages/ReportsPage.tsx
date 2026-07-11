import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { FileSpreadsheet, Download, FileText, CheckCircle2, AlertOctagon } from 'lucide-react';
import { PageContainer } from '../components/layout/PageContainer';
import { getStudents } from '../api/students';
import { generatePdfReport, generateDocxReport, getDownloadReportUrl } from '../api/reports';

export const ReportsPage: React.FC = () => {
  const { data: students = [], isLoading } = useQuery({
    queryKey: ['students-registry'],
    queryFn: getStudents
  });

  const handlePdfGen = async (studentId: string) => {
    try {
      const res = await generatePdfReport(studentId);
      window.open(getDownloadReportUrl(res.report_id), '_blank');
    } catch {
      alert("Failed to build PDF report. Ensure student has active risk predictions.");
    }
  };

  const handleDocxGen = async (studentId: string) => {
    try {
      const res = await generateDocxReport(studentId);
      window.open(getDownloadReportUrl(res.report_id), '_blank');
    } catch {
      alert("Failed to build DOCX report. Ensure student has active risk predictions.");
    }
  };

  if (isLoading) {
    return (
      <PageContainer>
        <div className="h-6 w-32 bg-slate-100 animate-pulse rounded" />
        <div className="h-96 bg-slate-100 animate-pulse rounded-2xl" />
      </PageContainer>
    );
  }

  return (
    <PageContainer>
      <div className="flex items-center gap-3 pb-2 border-b border-slate-100">
        <FileSpreadsheet className="h-6 w-6 text-blue-500" />
        <h2 className="text-xl font-bold tracking-tight">Intervention Reports Workspace</h2>
      </div>

      <div className="bg-white rounded-2xl border border-slate-100 shadow-sm overflow-hidden">
        <div className="p-4 bg-slate-50 border-b border-slate-100 flex items-center justify-between text-xs font-bold text-slate-400 uppercase tracking-wider">
          <span>Student Registry List</span>
          <span>Intervention Export actions</span>
        </div>

        <div className="divide-y divide-slate-100">
          {students.length === 0 ? (
            <div className="p-12 text-center text-slate-400 text-sm font-semibold">
              No students enrolled in registry yet.
            </div>
          ) : (
            students.map((student) => (
              <div 
                key={student.id} 
                className="p-5 flex flex-col sm:flex-row sm:items-center justify-between gap-4 hover:bg-slate-50/40 transition-colors"
              >
                <div>
                  <h4 className="font-bold text-slate-800 text-sm">{student.first_name} {student.last_name}</h4>
                  <span className="text-xs text-slate-400 font-bold">{student.student_code} • School: {student.school}</span>
                </div>
                <div className="flex items-center gap-3">
                  <button
                    onClick={() => handlePdfGen(student.id)}
                    className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-red-50 hover:bg-red-100 border border-red-100 text-red-700 text-xs font-bold rounded-xl transition-all shadow-sm"
                  >
                    <Download className="h-4 w-4" />
                    <span>Download PDF</span>
                  </button>
                  <button
                    onClick={() => handleDocxGen(student.id)}
                    className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-blue-50 hover:bg-blue-100 border border-blue-100 text-blue-700 text-xs font-bold rounded-xl transition-all shadow-sm"
                  >
                    <Download className="h-4 w-4" />
                    <span>Download Word</span>
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </PageContainer>
  );
};
