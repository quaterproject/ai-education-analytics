import React from 'react';
import { FileText, ClipboardList, CheckCircle, HelpCircle } from 'lucide-react';
import { Document } from '../../types/document';

interface ExtractedDataPreviewProps {
  document: Document;
}

export const ExtractedDataPreview: React.FC<ExtractedDataPreviewProps> = ({ document }) => {
  const data = document.structured_data;

  if (!data) {
    return (
      <div className="bg-slate-50 p-6 rounded-2xl border border-slate-100 flex items-center justify-center text-slate-400 text-sm h-40">
        <HelpCircle className="h-5 w-5 mr-2" />
        <span>No structured academic data extracted yet.</span>
      </div>
    );
  }

  return (
    <div className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm space-y-6">
      <div className="flex items-center gap-2 border-b border-slate-100 pb-3 text-slate-700">
        <FileText className="h-5 w-5 text-blue-500" />
        <h4 className="font-bold text-sm uppercase tracking-wide">Extracted Document Data</h4>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-xs font-semibold">
        {/* Basic Student Metadata */}
        <div className="space-y-4">
          <div>
            <span className="text-[10px] text-slate-400 uppercase tracking-wider block mb-1">Student Name</span>
            <p className="text-sm font-bold text-slate-800">{data.student_name || 'Not specified'}</p>
          </div>
          <div>
            <span className="text-[10px] text-slate-400 uppercase tracking-wider block mb-1">Student ID</span>
            <p className="text-sm font-bold text-slate-800">{data.student_id || 'Not specified'}</p>
          </div>
          <div>
            <span className="text-[10px] text-slate-400 uppercase tracking-wider block mb-1">Extracted Attendance</span>
            <p className="text-sm font-bold text-slate-800">
              {data.attendance !== null && data.attendance !== undefined
                ? `${data.attendance}%` 
                : 'Not specified'}
            </p>
          </div>
        </div>

        {/* Subjects & Grades */}
        <div className="space-y-3.5">
          <span className="text-[10px] text-slate-400 uppercase tracking-wider block">Subjects and Scores</span>
          {data.subjects && data.subjects.length > 0 ? (
            <div className="space-y-2 max-h-36 overflow-y-auto pr-1">
              {data.subjects.map((subject: string, idx: number) => {
                const grade = data.grades?.[idx];
                return (
                  <div key={idx} className="flex items-center justify-between p-2 bg-slate-50 rounded-lg border border-slate-100">
                    <span className="text-slate-700">{subject}</span>
                    <span className="font-bold px-2 py-0.5 bg-slate-100 rounded text-slate-700 border border-slate-200">
                      {grade !== undefined ? grade : '—'}
                    </span>
                  </div>
                );
              })}
            </div>
          ) : (
            <p className="text-slate-400 text-xs italic font-medium">No subjects found in extraction.</p>
          )}
        </div>

        {/* Comments */}
        <div className="col-span-1 md:col-span-2 space-y-2 border-t border-slate-100 pt-4">
          <span className="text-[10px] text-slate-400 uppercase tracking-wider block">Extracted Teacher Comments</span>
          {data.teacher_comments && data.teacher_comments.length > 0 ? (
            <ul className="space-y-2">
              {data.teacher_comments.map((comment: string, idx: number) => (
                <li key={idx} className="p-2.5 bg-blue-50/20 text-slate-600 rounded-xl border border-blue-50/50 leading-relaxed font-medium">
                  "{comment}"
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-slate-400 text-xs italic font-medium">No teacher notes found in document.</p>
          )}
        </div>
      </div>
    </div>
  );
};
