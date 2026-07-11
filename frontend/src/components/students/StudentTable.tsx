import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Search, ChevronRight, Filter, AlertCircle, AlertTriangle, CheckCircle, GraduationCap } from 'lucide-react';
import { Student } from '../../types/student';
import { cn } from '../../lib/utils';

interface StudentExtended extends Student {
  latest_risk?: 'LOW_RISK' | 'MEDIUM_RISK' | 'HIGH_RISK';
  confidence?: number;
  last_assessment?: string;
  review_status?: 'PENDING_REVIEW' | 'APPROVED' | 'REJECTED' | 'MODIFIED';
}

interface StudentTableProps {
  students: StudentExtended[];
}

export const StudentTable: React.FC<StudentTableProps> = ({ students }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [riskFilter, setRiskFilter] = useState<string>('ALL');
  const [schoolFilter, setSchoolFilter] = useState<string>('ALL');

  const filteredStudents = students.filter(student => {
    const fullName = `${student.first_name} ${student.last_name}`.toLowerCase();
    const code = student.student_code.toLowerCase();
    const matchesSearch = fullName.includes(searchTerm.toLowerCase()) || code.includes(searchTerm.toLowerCase());
    
    const matchesRisk = riskFilter === 'ALL' || student.latest_risk === riskFilter;
    const matchesSchool = schoolFilter === 'ALL' || student.school === schoolFilter;

    return matchesSearch && matchesRisk && matchesSchool;
  });

  const getRiskBadge = (level?: string) => {
    if (!level) return <span className="text-slate-400 text-xs font-semibold">N/A</span>;
    switch (level) {
      case 'HIGH_RISK':
        return (
          <span className="inline-flex items-center gap-1.5 px-3 py-1 bg-red-50 border border-red-100 text-red-700 text-xs font-semibold rounded-full shadow-sm">
            <span className="h-1.5 w-1.5 bg-red-500 rounded-full animate-ping" />
            <span>High Risk</span>
          </span>
        );
      case 'MEDIUM_RISK':
        return (
          <span className="inline-flex items-center gap-1.5 px-3 py-1 bg-amber-50 border border-amber-100 text-amber-700 text-xs font-semibold rounded-full shadow-sm">
            <span className="h-1.5 w-1.5 bg-amber-500 rounded-full" />
            <span>Medium Risk</span>
          </span>
        );
      default:
        return (
          <span className="inline-flex items-center gap-1.5 px-3 py-1 bg-emerald-50 border border-emerald-100 text-emerald-700 text-xs font-semibold rounded-full shadow-sm">
            <span className="h-1.5 w-1.5 bg-emerald-500 rounded-full" />
            <span>Low Risk</span>
          </span>
        );
    }
  };

  const getReviewBadge = (status?: string) => {
    if (!status) return <span className="text-slate-400 text-xs font-semibold">No Review</span>;
    switch (status) {
      case 'PENDING_REVIEW':
        return <span className="px-2 py-0.5 bg-purple-50 text-purple-700 text-[10px] font-bold border border-purple-100 rounded-md">PENDING</span>;
      case 'APPROVED':
        return <span className="px-2 py-0.5 bg-emerald-50 text-emerald-700 text-[10px] font-bold border border-emerald-100 rounded-md">APPROVED</span>;
      case 'REJECTED':
        return <span className="px-2 py-0.5 bg-red-50 text-red-700 text-[10px] font-bold border border-red-100 rounded-md">REJECTED</span>;
      case 'MODIFIED':
        return <span className="px-2 py-0.5 bg-amber-50 text-amber-700 text-[10px] font-bold border border-amber-100 rounded-md">MODIFIED</span>;
      default:
        return <span className="text-slate-400 text-xs font-semibold">N/A</span>;
    }
  };

  return (
    <div className="bg-white rounded-2xl border border-slate-100 shadow-sm overflow-hidden flex flex-col">
      {/* Table Filters Bar */}
      <div className="p-6 border-b border-slate-100 bg-slate-50/50 flex flex-col md:flex-row md:items-center justify-between gap-4">
        {/* Search */}
        <div className="relative flex-1 max-w-md">
          <span className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
            <Search className="h-4.5 w-4.5" />
          </span>
          <input
            type="text"
            placeholder="Search students by name or code..."
            className="w-full pl-10 pr-4 py-2 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 bg-white"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>

        {/* Filters */}
        <div className="flex flex-wrap items-center gap-3">
          <div className="flex items-center gap-2 text-xs font-bold text-slate-500">
            <Filter className="h-4 w-4 text-slate-400" />
            <span>FILTER BY</span>
          </div>
          
          {/* Risk Filter */}
          <select
            className="px-3 py-1.5 border border-slate-200 rounded-lg text-xs font-semibold text-slate-600 focus:outline-none bg-white"
            value={riskFilter}
            onChange={(e) => setRiskFilter(e.target.value)}
          >
            <option value="ALL">All Risk Levels</option>
            <option value="HIGH_RISK">High Risk</option>
            <option value="MEDIUM_RISK">Medium Risk</option>
            <option value="LOW_RISK">Low Risk</option>
          </select>

          {/* School Filter */}
          <select
            className="px-3 py-1.5 border border-slate-200 rounded-lg text-xs font-semibold text-slate-600 focus:outline-none bg-white"
            value={schoolFilter}
            onChange={(e) => setSchoolFilter(e.target.value)}
          >
            <option value="ALL">All Schools</option>
            <option value="GP">Gabriel Pereira (GP)</option>
            <option value="MS">Mousinho da Silveira (MS)</option>
          </select>
        </div>
      </div>

      {/* Table Data */}
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-slate-50/70 border-b border-slate-100 text-xs font-bold text-slate-400 tracking-wider">
              <th className="p-4 pl-6">Student</th>
              <th className="p-4">School</th>
              <th className="p-4">Latest Risk</th>
              <th className="p-4">Confidence</th>
              <th className="p-4">Last Assessment</th>
              <th className="p-4">Review Status</th>
              <th className="p-4 text-right pr-6">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 text-sm font-medium text-slate-700">
            {filteredStudents.length === 0 ? (
              <tr>
                <td colSpan={7} className="p-12 text-center text-slate-400 text-sm">
                  No students matching your search criteria were found.
                </td>
              </tr>
            ) : (
              filteredStudents.map((student) => (
                <tr 
                  key={student.id} 
                  className="hover:bg-slate-50/40 transition-colors duration-150"
                >
                  <td className="p-4 pl-6">
                    <div>
                      <span className="font-bold text-slate-800 text-sm block">{student.first_name} {student.last_name}</span>
                      <span className="text-xs text-slate-400 font-bold">{student.student_code}</span>
                    </div>
                  </td>
                  <td className="p-4">
                    <span className="text-xs font-bold px-2 py-0.5 bg-slate-100 text-slate-600 border border-slate-200 rounded-md">
                      {student.school}
                    </span>
                  </td>
                  <td className="p-4">{getRiskBadge(student.latest_risk)}</td>
                  <td className="p-4">
                    {student.confidence !== undefined ? (
                      <span className="text-slate-600 font-bold">{Math.round(student.confidence * 100)}%</span>
                    ) : (
                      <span className="text-slate-400 font-semibold">—</span>
                    )}
                  </td>
                  <td className="p-4">
                    {student.last_assessment ? (
                      <span className="text-slate-500 text-xs font-semibold">{new Date(student.last_assessment).toLocaleDateString()}</span>
                    ) : (
                      <span className="text-slate-400 text-xs font-semibold">Not Assessed</span>
                    )}
                  </td>
                  <td className="p-4">{getReviewBadge(student.review_status)}</td>
                  <td className="p-4 text-right pr-6">
                    <Link
                      to={`/students/${student.id}`}
                      className="inline-flex items-center gap-1 text-xs font-bold text-blue-600 hover:text-blue-700 transition-colors duration-150"
                    >
                      <span>Profile</span>
                      <ChevronRight className="h-4 w-4" />
                    </Link>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};
