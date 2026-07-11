import React, { useState, useRef } from 'react';
import { Upload, File, AlertCircle, FileText, CheckCircle, Image as ImageIcon } from 'lucide-react';
import { cn } from '../../lib/utils';

interface DocumentUploaderProps {
  onUpload: (file: File) => void;
  isUploading: boolean;
  allowedTypes?: string[];
  maxSizeMB?: number;
}

export const DocumentUploader: React.FC<DocumentUploaderProps> = ({
  onUpload,
  isUploading,
  allowedTypes = ['.pdf', '.png', '.jpg', '.jpeg', '.webp'],
  maxSizeMB = 10
}) => {
  const [dragActive, setDragActive] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [error, setError] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const validateFile = (file: File): boolean => {
    setError(null);
    const ext = `.${file.name?.split('.').pop()?.toLowerCase() || ''}`;
    
    // Check type
    if (!allowedTypes.includes(ext)) {
      setError(`Invalid file type. Allowed formats: ${allowedTypes.join(', ')}`);
      return false;
    }
    
    // Check size
    const sizeMB = file.size / (1024 * 1024);
    if (sizeMB > maxSizeMB) {
      setError(`File size exceeds maximum limit of ${maxSizeMB}MB.`);
      return false;
    }
    
    return true;
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      if (validateFile(file)) {
        setSelectedFile(file);
      }
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      if (validateFile(file)) {
        setSelectedFile(file);
      }
    }
  };

  const triggerUpload = () => {
    if (selectedFile) {
      onUpload(selectedFile);
    }
  };

  const clearSelection = () => {
    setSelectedFile(null);
    setError(null);
  };

  return (
    <div className="space-y-4">
      {/* Upload Box Area */}
      <div 
        onDragEnter={handleDrag}
        onDragOver={handleDrag}
        onDragLeave={handleDrag}
        onDrop={handleDrop}
        className={cn(
          "border-2 border-dashed rounded-2xl p-8 flex flex-col items-center justify-center text-center transition-all duration-300 min-h-[220px]",
          dragActive ? "border-blue-500 bg-blue-50/30" : "border-slate-200 bg-slate-50/30 hover:border-slate-300",
          selectedFile ? "border-emerald-200 bg-emerald-50/10" : ""
        )}
      >
        <input 
          ref={inputRef}
          type="file" 
          className="hidden" 
          onChange={handleFileChange}
          accept={allowedTypes.join(',')}
          disabled={isUploading}
        />

        {selectedFile ? (
          // File selected state
          <div className="space-y-4">
            <div className="p-3.5 bg-emerald-50 border border-emerald-100 rounded-2xl inline-flex text-emerald-600">
              {selectedFile.name.endsWith('.pdf') ? (
                <FileText className="h-8 w-8" />
              ) : (
                <ImageIcon className="h-8 w-8" />
              )}
            </div>
            <div>
              <p className="text-sm font-bold text-slate-800">{selectedFile.name}</p>
              <p className="text-[10px] text-slate-400 font-semibold mt-0.5">
                {(selectedFile.size / 1024).toFixed(1)} KB
              </p>
            </div>
            
            <div className="flex items-center gap-3 justify-center">
              <button
                type="button"
                onClick={clearSelection}
                className="px-3.5 py-1.5 border border-slate-200 text-slate-500 rounded-xl text-xs font-bold hover:bg-slate-50 transition-colors"
                disabled={isUploading}
              >
                Clear
              </button>
              <button
                type="button"
                onClick={triggerUpload}
                className="px-4 py-1.5 bg-blue-600 hover:bg-blue-700 text-white rounded-xl text-xs font-bold transition-all shadow-md shadow-blue-600/10"
                disabled={isUploading}
              >
                {isUploading ? 'Uploading...' : 'Extract Data'}
              </button>
            </div>
          </div>
        ) : (
          // Drag state
          <div className="space-y-3 cursor-pointer" onClick={() => inputRef.current?.click()}>
            <div className="p-3.5 bg-white border border-slate-100 rounded-2xl inline-flex text-slate-400 shadow-sm transition-transform duration-300 hover:scale-105">
              <Upload className="h-7 w-7 text-blue-500" />
            </div>
            <div>
              <p className="text-sm font-bold text-slate-700">Drag and drop file here</p>
              <p className="text-xs text-slate-400 font-semibold mt-0.5">
                or click to browse local reports
              </p>
            </div>
            <span className="text-[10px] font-bold text-slate-400 block tracking-wide">
              PDF, PNG, JPG, JPEG, WEBP up to {maxSizeMB}MB
            </span>
          </div>
        )}
      </div>

      {error && (
        <div className="p-3 bg-red-50 text-red-700 text-xs font-semibold rounded-lg border border-red-100 flex items-center gap-2">
          <AlertCircle className="h-4 w-4 shrink-0" />
          <span>{error}</span>
        </div>
      )}
    </div>
  );
};
