import React from 'react';
import { User, School, Calendar, Activity } from 'lucide-react';
import { Student } from '../../types/student';

interface StudentProfileCardProps {
  student: Student;
}

export const StudentProfileCard: React.FC<StudentProfileCardProps> = ({ student }) => {
  return (
    <div className="bg-gradient-to-r from-slate-900 to-indigo-950 p-6 rounded-2xl text-slate-100 shadow-lg border border-slate-800 flex flex-col md:flex-row md:items-center justify-between gap-6">
      {/* Profile Info */}
      <div className="flex items-center gap-4">
        <div className="h-16 w-16 bg-white/10 rounded-2xl flex items-center justify-center font-bold text-2xl text-blue-400 border border-white/10 shadow-inner">
          {student.first_name.charAt(0)}{student.last_name.charAt(0)}
        </div>
        <div>
          <span className="text-[10px] font-bold tracking-widest text-blue-400 bg-blue-400/10 px-2.5 py-1 rounded-full border border-blue-400/20 uppercase">
            Student Profile
          </span>
          <h2 className="text-2xl font-bold mt-1.5 tracking-tight text-white">
            {student.first_name} {student.last_name}
          </h2>
          <p className="text-xs text-slate-400 font-semibold mt-0.5">Code: {student.student_code}</p>
        </div>
      </div>

      {/* Mini details grid */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 md:gap-8 pt-4 md:pt-0 border-t md:border-t-0 md:border-l border-white/10 pl-0 md:pl-8">
        <div>
          <span className="text-[10px] text-slate-500 font-bold uppercase block mb-1">School</span>
          <div className="flex items-center gap-1.5 text-sm font-semibold text-slate-200">
            <School className="h-4 w-4 text-blue-400" />
            <span>{student.school === 'GP' ? 'Gabriel Pereira' : 'Mousinho Silveira'}</span>
          </div>
        </div>

        <div>
          <span className="text-[10px] text-slate-500 font-bold uppercase block mb-1">Age</span>
          <div className="flex items-center gap-1.5 text-sm font-semibold text-slate-200">
            <Calendar className="h-4 w-4 text-blue-400" />
            <span>{student.age} years old</span>
          </div>
        </div>

        <div>
          <span className="text-[10px] text-slate-500 font-bold uppercase block mb-1">Gender</span>
          <div className="flex items-center gap-1.5 text-sm font-semibold text-slate-200">
            <User className="h-4 w-4 text-blue-400" />
            <span>{student.gender === 'F' ? 'Female' : 'Male'}</span>
          </div>
        </div>

        <div>
          <span className="text-[10px] text-slate-500 font-bold uppercase block mb-1">Created At</span>
          <div className="flex items-center gap-1.5 text-sm font-semibold text-slate-200">
            <Activity className="h-4 w-4 text-blue-400" />
            <span>{new Date(student.created_at).toLocaleDateString()}</span>
          </div>
        </div>
      </div>
    </div>
  );
};
