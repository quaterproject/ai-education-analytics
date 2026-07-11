import React, { useState } from 'react';
import { X, Check } from 'lucide-react';
import { Student } from '../../types/student';
import { cn } from '../../lib/utils';

export type StudentCreate = Omit<Student, 'id' | 'created_at' | 'updated_at'>;

interface StudentFormProps {
  onSubmit: (student: StudentCreate) => void;
  onCancel: () => void;
  isSubmitting?: boolean;
}

export const StudentForm: React.FC<StudentFormProps> = ({ onSubmit, onCancel, isSubmitting }) => {
  const [code, setCode] = useState('');
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [age, setAge] = useState(16);
  const [gender, setGender] = useState<'M' | 'F'>('F');
  const [school, setSchool] = useState<'GP' | 'MS'>('GP');
  const [error, setError] = useState<string | null>(null);

  const handleFormSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    
    if (!code.trim() || !firstName.trim() || !lastName.trim()) {
      setError("Please fill out all required fields.");
      return;
    }
    
    onSubmit({
      student_code: code.trim().toUpperCase(),
      first_name: firstName.trim(),
      last_name: lastName.trim(),
      age: Number(age),
      gender: gender,
      school: school
    });
  };

  return (
    <form onSubmit={handleFormSubmit} className="space-y-5 bg-white p-6 rounded-2xl border border-slate-100 shadow-sm max-w-lg w-full">
      <div className="flex items-center justify-between pb-3 border-b border-slate-100">
        <h3 className="font-bold text-slate-800 text-base">Register New Student</h3>
        <button 
          type="button" 
          onClick={onCancel}
          className="p-1 rounded-lg text-slate-400 hover:bg-slate-50 hover:text-slate-600 transition-colors"
        >
          <X className="h-5 w-5" />
        </button>
      </div>

      {error && (
        <div className="p-3 bg-red-50 text-red-700 text-xs font-semibold rounded-lg border border-red-100">
          {error}
        </div>
      )}

      <div className="grid grid-cols-2 gap-4">
        {/* Student Code */}
        <div className="col-span-2">
          <label className="block text-xs font-bold text-slate-500 mb-1.5 uppercase">Student Code / ID</label>
          <input
            type="text"
            placeholder="e.g. GP-512"
            className="w-full px-3.5 py-2 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 bg-slate-50/50"
            value={code}
            onChange={(e) => setCode(e.target.value)}
            disabled={isSubmitting}
            required
          />
        </div>

        {/* First Name */}
        <div>
          <label className="block text-xs font-bold text-slate-500 mb-1.5 uppercase">First Name</label>
          <input
            type="text"
            placeholder="e.g. John"
            className="w-full px-3.5 py-2 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 bg-slate-50/50"
            value={firstName}
            onChange={(e) => setFirstName(e.target.value)}
            disabled={isSubmitting}
            required
          />
        </div>

        {/* Last Name */}
        <div>
          <label className="block text-xs font-bold text-slate-500 mb-1.5 uppercase">Last Name</label>
          <input
            type="text"
            placeholder="e.g. Doe"
            className="w-full px-3.5 py-2 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 bg-slate-50/50"
            value={lastName}
            onChange={(e) => setLastName(e.target.value)}
            disabled={isSubmitting}
            required
          />
        </div>

        {/* Age */}
        <div>
          <label className="block text-xs font-bold text-slate-500 mb-1.5 uppercase">Age</label>
          <input
            type="number"
            min={12}
            max={25}
            className="w-full px-3.5 py-2 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 bg-slate-50/50"
            value={age}
            onChange={(e) => setAge(Number(e.target.value))}
            disabled={isSubmitting}
            required
          />
        </div>

        {/* Gender */}
        <div>
          <label className="block text-xs font-bold text-slate-500 mb-1.5 uppercase">Gender</label>
          <div className="grid grid-cols-2 gap-2">
            <button
              type="button"
              className={cn(
                "py-2 text-xs font-bold border rounded-xl transition-all duration-200",
                gender === 'F' 
                  ? "bg-blue-50 text-blue-700 border-blue-200 shadow-sm" 
                  : "bg-slate-50/50 text-slate-500 border-slate-200 hover:bg-slate-100/50"
              )}
              onClick={() => setGender('F')}
              disabled={isSubmitting}
            >
              Female
            </button>
            <button
              type="button"
              className={cn(
                "py-2 text-xs font-bold border rounded-xl transition-all duration-200",
                gender === 'M' 
                  ? "bg-blue-50 text-blue-700 border-blue-200 shadow-sm" 
                  : "bg-slate-50/50 text-slate-500 border-slate-200 hover:bg-slate-100/50"
              )}
              onClick={() => setGender('M')}
              disabled={isSubmitting}
            >
              Male
            </button>
          </div>
        </div>

        {/* School */}
        <div className="col-span-2">
          <label className="block text-xs font-bold text-slate-500 mb-1.5 uppercase">School Affiliate</label>
          <div className="grid grid-cols-2 gap-2.5">
            <button
              type="button"
              className={cn(
                "py-2.5 text-xs font-bold border rounded-xl transition-all duration-200 flex flex-col items-center justify-center",
                school === 'GP' 
                  ? "bg-blue-50 text-blue-700 border-blue-200 shadow-sm" 
                  : "bg-slate-50/50 text-slate-500 border-slate-200 hover:bg-slate-100/50"
              )}
              onClick={() => setSchool('GP')}
              disabled={isSubmitting}
            >
              <span className="font-bold">Gabriel Pereira</span>
              <span className="text-[9px] opacity-70 font-semibold">GP</span>
            </button>
            <button
              type="button"
              className={cn(
                "py-2.5 text-xs font-bold border rounded-xl transition-all duration-200 flex flex-col items-center justify-center",
                school === 'MS' 
                  ? "bg-blue-50 text-blue-700 border-blue-200 shadow-sm" 
                  : "bg-slate-50/50 text-slate-500 border-slate-200 hover:bg-slate-100/50"
              )}
              onClick={() => setSchool('MS')}
              disabled={isSubmitting}
            >
              <span className="font-bold">Mousinho da Silveira</span>
              <span className="text-[9px] opacity-70 font-semibold">MS</span>
            </button>
          </div>
        </div>
      </div>

      <div className="flex items-center justify-end gap-3 pt-3 border-t border-slate-100">
        <button
          type="button"
          onClick={onCancel}
          className="px-4 py-2 border border-slate-200 rounded-xl text-xs font-bold text-slate-500 hover:bg-slate-50 transition-colors"
          disabled={isSubmitting}
        >
          Cancel
        </button>
        <button
          type="submit"
          className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-xl text-xs font-bold flex items-center gap-1.5 transition-all duration-200 shadow-lg shadow-blue-600/10 disabled:opacity-50"
          disabled={isSubmitting}
        >
          {isSubmitting ? (
            <span>Saving...</span>
          ) : (
            <>
              <Check className="h-4 w-4" />
              <span>Register Student</span>
            </>
          )}
        </button>
      </div>
    </form>
  );
};
