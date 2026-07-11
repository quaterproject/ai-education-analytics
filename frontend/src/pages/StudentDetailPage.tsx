import React, { useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { 
  ArrowLeft, 
  Activity, 
  BrainCircuit, 
  FileText, 
  Plus, 
  FolderPlus, 
  Play,
  FileSpreadsheet,
  Download,
  AlertTriangle,
  ClipboardList
} from 'lucide-react';

import { PageContainer } from '../components/layout/PageContainer';
import { StudentProfileCard } from '../components/students/StudentProfileCard';
import { RiskScoreCard } from '../components/prediction/RiskScoreCard';
import { ConfidenceGauge } from '../components/prediction/ConfidenceGauge';
import { FeatureImportanceChart } from '../components/prediction/FeatureImportanceChart';
import { RiskFactors } from '../components/prediction/RiskFactors';
import { ProtectiveFactors } from '../components/prediction/ProtectiveFactors';
import { DocumentUploader } from '../components/documents/DocumentUploader';
import { ExtractedDataPreview } from '../components/documents/ExtractedDataPreview';
import { ProcessingStatus, StepStatus } from '../components/documents/ProcessingStatus';
import { RecommendationCard } from '../components/recommendations/RecommendationCard';
import { InterventionPlan } from '../components/recommendations/InterventionPlan';
import { HumanReviewPanel } from '../components/reviews/HumanReviewPanel';

import { getStudent, getAcademicRecords, addAcademicRecord } from '../api/students';
import { predictStudentRisk, getStudentPredictions, generateRecommendation } from '../api/predictions';
import { listStudentDocuments, uploadDocument } from '../api/documents';
import { approveRecommendation, rejectRecommendation, modifyRecommendation, getPendingReviews } from '../api/reviews';
import { generatePdfReport, generateDocxReport, getDownloadReportUrl } from '../api/reports';
import { cn } from '../lib/utils';

export const StudentDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const queryClient = useQueryClient();
  const studentId = id || '';

  // Tab view controller
  const [activeTab, setActiveTab] = useState<'ASSESSMENT' | 'ACADEMICS' | 'DOCUMENTS'>('ASSESSMENT');

  // New academic record form fields
  const [showRecordForm, setShowRecordForm] = useState(false);
  const [studyTime, setStudyTime] = useState(2);
  const [failures, setFailures] = useState(0);
  const [absences, setAbsences] = useState(2);
  const [familySupport, setFamilySupport] = useState<'yes' | 'no'>('yes');
  const [schoolSupport, setSchoolSupport] = useState<'yes' | 'no'>('no');
  const [internet, setInternet] = useState<'yes' | 'no'>('yes');
  const [health, setHealth] = useState(4);
  const [g1, setG1] = useState(12);
  const [g2, setG2] = useState(12);

  // AI Pipeline run steps tracking
  const [pipelineActive, setPipelineActive] = useState(false);
  const [pipelineSteps, setPipelineSteps] = useState<StepStatus[]>([]);

  // Document upload state
  const [isUploading, setIsUploading] = useState(false);

  // Queries
  const { data: student, isLoading: isStudentLoading } = useQuery({
    queryKey: ['student-details', studentId],
    queryFn: () => getStudent(studentId),
    enabled: !!studentId
  });

  const { data: records = [], isLoading: isRecordsLoading } = useQuery({
    queryKey: ['student-records', studentId],
    queryFn: () => getAcademicRecords(studentId),
    enabled: !!studentId
  });

  const { data: documents = [], isLoading: isDocsLoading } = useQuery({
    queryKey: ['student-documents', studentId],
    queryFn: () => listStudentDocuments(studentId),
    enabled: !!studentId
  });

  const { data: predictions = [], isLoading: isPredictsLoading } = useQuery({
    queryKey: ['student-predictions', studentId],
    queryFn: () => getStudentPredictions(studentId),
    enabled: !!studentId
  });

  const { data: pendingReviews = [] } = useQuery({
    queryKey: ['pending-reviews-list'],
    queryFn: getPendingReviews
  });

  // Mutations
  const recordMutation = useMutation({
    mutationFn: (data: any) => addAcademicRecord(studentId, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['student-records', studentId] });
      setShowRecordForm(false);
    }
  });

  const predictMutation = useMutation({
    mutationFn: (args: { studentId: string; modelType: 'EARLY_WARNING' | 'LATE_STAGE' }) => 
      predictStudentRisk(args.studentId, args.modelType),
    onSuccess: (prediction) => {
      queryClient.invalidateQueries({ queryKey: ['student-predictions', studentId] });
    }
  });

  const uploadMutation = useMutation({
    mutationFn: (file: File) => uploadDocument(studentId, file),
    onSuccess: (doc) => {
      queryClient.invalidateQueries({ queryKey: ['student-documents', studentId] });
      setIsUploading(false);
    },
    onError: () => {
      setIsUploading(false);
    }
  });

  // Educator reviews action triggers
  const handleApprove = async (reviewedBy: string, comment?: string) => {
    const currentRec = predictions[0]?.recommendation;
    if (!currentRec) return;
    await approveRecommendation(currentRec.id, reviewedBy, comment);
    queryClient.invalidateQueries({ queryKey: ['student-predictions', studentId] });
    queryClient.invalidateQueries({ queryKey: ['pending-reviews-list'] });
    queryClient.invalidateQueries({ queryKey: ['analytics-overview'] });
  };

  const handleReject = async (reviewedBy: string, reason: string) => {
    const currentRec = predictions[0]?.recommendation;
    if (!currentRec) return;
    await rejectRecommendation(currentRec.id, reviewedBy, reason);
    queryClient.invalidateQueries({ queryKey: ['student-predictions', studentId] });
    queryClient.invalidateQueries({ queryKey: ['pending-reviews-list'] });
    queryClient.invalidateQueries({ queryKey: ['analytics-overview'] });
  };

  const handleModify = async (reviewedBy: string, comment: string, modifiedData: any) => {
    const currentRec = predictions[0]?.recommendation;
    if (!currentRec) return;
    await modifyRecommendation(currentRec.id, reviewedBy, comment, modifiedData);
    queryClient.invalidateQueries({ queryKey: ['student-predictions', studentId] });
    queryClient.invalidateQueries({ queryKey: ['pending-reviews-list'] });
    queryClient.invalidateQueries({ queryKey: ['analytics-overview'] });
  };

  // Run AI Risk Pipeline
  const runAssessmentPipeline = async (modelType: 'EARLY_WARNING' | 'LATE_STAGE') => {
    setPipelineActive(true);
    const steps: StepStatus[] = [
      { id: '1', label: 'Processing academic data...', status: 'RUNNING' },
      { id: '2', label: 'Running PyTorch ANN risk model...', status: 'PENDING' },
      { id: '3', label: 'Calculating SHAP feature explanations...', status: 'PENDING' },
      { id: '4', label: 'Generating LLM intervention recommendations...', status: 'PENDING' },
    ];
    setPipelineSteps(steps);

    try {
      // Step 1: Academic check
      await new Promise(r => setTimeout(r, 1200));
      setPipelineSteps(prev => prev.map(s => s.id === '1' ? { ...s, status: 'COMPLETED' } : (s.id === '2' ? { ...s, status: 'RUNNING' } : s)));
      
      // Step 2: Run ANN risk model
      const prediction = await predictMutation.mutateAsync({ studentId, modelType });
      setPipelineSteps(prev => prev.map(s => s.id === '2' ? { ...s, status: 'COMPLETED' } : (s.id === '3' ? { ...s, status: 'RUNNING' } : s)));
      
      // Step 3: SHAP
      await new Promise(r => setTimeout(r, 1500));
      setPipelineSteps(prev => prev.map(s => s.id === '3' ? { ...s, status: 'COMPLETED' } : (s.id === '4' ? { ...s, status: 'RUNNING' } : s)));
      
      // Step 4: Generate recommendations via LLM
      await generateRecommendation(prediction.id);
      setPipelineSteps(prev => prev.map(s => s.id === '4' ? { ...s, status: 'COMPLETED' } : s));
      
      await new Promise(r => setTimeout(r, 800));
      queryClient.invalidateQueries({ queryKey: ['student-predictions', studentId] });
      queryClient.invalidateQueries({ queryKey: ['pending-reviews-list'] });
      queryClient.invalidateQueries({ queryKey: ['analytics-overview'] });
      setPipelineActive(false);
    } catch (err) {
      setPipelineSteps(prev => prev.map(s => s.status === 'RUNNING' ? { ...s, status: 'FAILED' } : s));
      setPipelineActive(false);
    }
  };

  // Upload Document Trigger
  const handleUploadDocument = (file: File) => {
    setIsUploading(true);
    uploadMutation.mutate(file);
  };

  // Generate Report triggers
  const triggerPdfDownload = async () => {
    try {
      const response = await generatePdfReport(studentId);
      window.open(getDownloadReportUrl(response.report_id), '_blank');
    } catch (err) {
      alert("Failed to generate PDF report.");
    }
  };

  const triggerDocxDownload = async () => {
    try {
      const response = await generateDocxReport(studentId);
      window.open(getDownloadReportUrl(response.report_id), '_blank');
    } catch (err) {
      alert("Failed to generate Word report.");
    }
  };

  if (isStudentLoading || isRecordsLoading || isDocsLoading || isPredictsLoading) {
    return (
      <PageContainer>
        <div className="h-6 w-32 bg-slate-100 animate-pulse rounded" />
        <div className="h-32 bg-slate-100 animate-pulse rounded-2xl" />
        <div className="h-96 bg-slate-100 animate-pulse rounded-2xl" />
      </PageContainer>
    );
  }

  if (!student) {
    return (
      <PageContainer>
        <div className="text-center p-12 text-slate-500 font-semibold">
          Student not found.
        </div>
      </PageContainer>
    );
  }

  // Identify latest assessment values
  const latestPrediction = predictions[0];
  const latestReview = latestPrediction?.recommendation?.review;

  const handleAddRecordSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    recordMutation.mutate({
      study_time: studyTime,
      failures: failures,
      absences: absences,
      family_support: familySupport,
      school_support: schoolSupport,
      internet_access: internet,
      health: health,
      g1: g1,
      g2: g2
    });
  };

  return (
    <PageContainer>
      {/* Back navigation & reports panel */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <Link 
          to="/students" 
          className="inline-flex items-center gap-1.5 text-xs font-bold text-slate-500 hover:text-slate-700 transition-colors"
        >
          <ArrowLeft className="h-4.5 w-4.5" />
          <span>Back to Registry</span>
        </Link>

        {/* Report downloads */}
        {latestPrediction && (
          <div className="flex items-center gap-2">
            <button
              onClick={triggerPdfDownload}
              className="inline-flex items-center gap-1.5 px-3 py-2 bg-red-600 hover:bg-red-700 text-white rounded-xl text-xs font-bold transition-all shadow-md shadow-red-600/10"
            >
              <Download className="h-4 w-4" />
              <span>Generate PDF Report</span>
            </button>
            <button
              onClick={triggerDocxDownload}
              className="inline-flex items-center gap-1.5 px-3 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-xl text-xs font-bold transition-all shadow-md shadow-blue-600/10"
            >
              <Download className="h-4 w-4" />
              <span>Generate Word DOCX</span>
            </button>
          </div>
        )}
      </div>

      {/* Student Profile Overview */}
      <StudentProfileCard student={student} />

      {/* Tab controller */}
      <div className="flex items-center border-b border-slate-200 gap-6">
        <button
          onClick={() => setActiveTab('ASSESSMENT')}
          className={cn(
            "pb-3.5 text-xs font-extrabold tracking-wide uppercase border-b-2 transition-all duration-200",
            activeTab === 'ASSESSMENT' ? "border-blue-600 text-blue-600" : "border-transparent text-slate-400 hover:text-slate-600"
          )}
        >
          Risk Assessment
        </button>
        <button
          onClick={() => setActiveTab('ACADEMICS')}
          className={cn(
            "pb-3.5 text-xs font-extrabold tracking-wide uppercase border-b-2 transition-all duration-200",
            activeTab === 'ACADEMICS' ? "border-blue-600 text-blue-600" : "border-transparent text-slate-400 hover:text-slate-600"
          )}
        >
          Academic Records ({records.length})
        </button>
        <button
          onClick={() => setActiveTab('DOCUMENTS')}
          className={cn(
            "pb-3.5 text-xs font-extrabold tracking-wide uppercase border-b-2 transition-all duration-200",
            activeTab === 'DOCUMENTS' ? "border-blue-600 text-blue-600" : "border-transparent text-slate-400 hover:text-slate-600"
          )}
        >
          Multimodal Files ({documents.length})
        </button>
      </div>

      {/* Tab content panel */}
      <div className="space-y-6">
        {/* tab 1: Risk assessment explanations */}
        {activeTab === 'ASSESSMENT' && (
          <div className="space-y-6">
            {pipelineActive && (
              <div className="flex justify-center p-6">
                <ProcessingStatus steps={pipelineSteps} />
              </div>
            )}

            {!latestPrediction && !pipelineActive ? (
              // Prompt to run assessment
              <div className="bg-slate-50 border border-slate-200 p-8 rounded-2xl text-center space-y-4 max-w-xl mx-auto">
                <BrainCircuit className="h-10 w-10 text-blue-500 mx-auto animate-pulse" />
                <div>
                  <h3 className="font-bold text-slate-800 text-base">No Risk Analysis Recorded</h3>
                  <p className="text-xs text-slate-500 font-semibold leading-relaxed mt-1">
                    Execute the PyTorch predictive engine and explainability matrices using the recorded performance logs.
                  </p>
                </div>
                {records.length === 0 ? (
                  <p className="text-xs text-red-500 font-bold bg-red-50 border border-red-100 p-2.5 rounded-xl">
                    Warning: Add at least one academic record to initialize the assessment.
                  </p>
                ) : (
                  <div className="flex items-center gap-3 justify-center">
                    <button
                      onClick={() => runAssessmentPipeline('EARLY_WARNING')}
                      className="inline-flex items-center gap-1 px-4 py-2.5 bg-blue-50 border border-blue-200 text-blue-700 rounded-xl text-xs font-bold hover:bg-blue-100 transition-colors"
                    >
                      <Play className="h-3.5 w-3.5" />
                      <span>Run Early Warning (No Exam Grades)</span>
                    </button>
                    <button
                      onClick={() => runAssessmentPipeline('LATE_STAGE')}
                      className="inline-flex items-center gap-1 px-4 py-2.5 bg-blue-600 hover:bg-blue-700 text-white rounded-xl text-xs font-bold transition-all shadow-md shadow-blue-600/10"
                    >
                      <Play className="h-3.5 w-3.5" />
                      <span>Run Late Stage (Include G1/G2 Grades)</span>
                    </button>
                  </div>
                )}
              </div>
            ) : (
              // Assessment Dashboard
              latestPrediction && !pipelineActive && (
                <div className="space-y-6">
                  {/* Risk & Confidence overview */}
                  <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    <div className="lg:col-span-2">
                      <RiskScoreCard 
                        riskLevel={latestPrediction.risk_level} 
                        confidence={latestPrediction.confidence} 
                      />
                    </div>
                    <div>
                      <ConfidenceGauge confidence={latestPrediction.confidence} />
                    </div>
                  </div>

                  {/* SHAP Explanations & Driver Lists */}
                  <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    <div className="lg:col-span-2">
                      <FeatureImportanceChart shapValues={latestPrediction.shap_values} />
                    </div>
                    <div className="space-y-6">
                      <RiskFactors factors={latestPrediction.risk_factors} />
                      <ProtectiveFactors factors={latestPrediction.protective_factors} />
                    </div>
                  </div>

                  {/* Recommendations */}
                  {latestPrediction.recommendation && (
                    <div className="space-y-6">
                      <RecommendationCard recommendation={latestPrediction.recommendation} />
                      
                      <InterventionPlan
                        recommendedActions={latestPrediction.recommendation.recommended_actions}
                        monitoringPlan={latestPrediction.recommendation.monitoring_plan}
                        successIndicators={latestPrediction.recommendation.success_indicators}
                      />

                      {/* HITL review component */}
                      {latestPrediction.recommendation.review && (
                        <HumanReviewPanel
                          recommendation={latestPrediction.recommendation}
                          review={latestPrediction.recommendation.review}
                          onApprove={handleApprove}
                          onReject={handleReject}
                          onModify={handleModify}
                        />
                      )}
                    </div>
                  )}
                </div>
              )
            )}
          </div>
        )}

        {/* tab 2: Academic records manager */}
        {activeTab === 'ACADEMICS' && (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <h3 className="font-bold text-slate-800 text-base">Academic History</h3>
              <button
                onClick={() => setShowRecordForm(true)}
                className="inline-flex items-center gap-1 px-3 py-1.5 bg-blue-600 hover:bg-blue-700 text-white rounded-xl text-xs font-bold transition-all shadow-md shadow-blue-600/10"
              >
                <Plus className="h-4 w-4" />
                <span>Log Performance Record</span>
              </button>
            </div>

            {showRecordForm && (
              <form onSubmit={handleAddRecordSubmit} className="p-6 bg-slate-50 border border-slate-200 rounded-2xl max-w-2xl space-y-4">
                <h4 className="text-xs font-extrabold text-slate-700 uppercase tracking-wide">Enter Performance Values</h4>
                <div className="grid grid-cols-2 sm:grid-cols-3 gap-4 text-xs">
                  <div>
                    <label className="block text-slate-500 font-bold mb-1">Study Time (hours/week)</label>
                    <input type="number" min={1} max={4} className="w-full px-3 py-2 border rounded-lg bg-white font-semibold" value={studyTime} onChange={(e) => setStudyTime(Number(e.target.value))} required />
                  </div>
                  <div>
                    <label className="block text-slate-500 font-bold mb-1">Previous Failures</label>
                    <input type="number" min={0} max={3} className="w-full px-3 py-2 border rounded-lg bg-white font-semibold" value={failures} onChange={(e) => setFailures(Number(e.target.value))} required />
                  </div>
                  <div>
                    <label className="block text-slate-500 font-bold mb-1">Absences</label>
                    <input type="number" min={0} max={93} className="w-full px-3 py-2 border rounded-lg bg-white font-semibold" value={absences} onChange={(e) => setAbsences(Number(e.target.value))} required />
                  </div>
                  <div>
                    <label className="block text-slate-500 font-bold mb-1">Family Support</label>
                    <select className="w-full px-3 py-2 border rounded-lg bg-white font-semibold" value={familySupport} onChange={(e) => setFamilySupport(e.target.value as any)}>
                      <option value="yes">Yes</option>
                      <option value="no">No</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-slate-500 font-bold mb-1">School Support</label>
                    <select className="w-full px-3 py-2 border rounded-lg bg-white font-semibold" value={schoolSupport} onChange={(e) => setSchoolSupport(e.target.value as any)}>
                      <option value="yes">Yes</option>
                      <option value="no">No</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-slate-500 font-bold mb-1">Internet Access</label>
                    <select className="w-full px-3 py-2 border rounded-lg bg-white font-semibold" value={internet} onChange={(e) => setInternet(e.target.value as any)}>
                      <option value="yes">Yes</option>
                      <option value="no">No</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-slate-500 font-bold mb-1">Health Index (1-5)</label>
                    <input type="number" min={1} max={5} className="w-full px-3 py-2 border rounded-lg bg-white font-semibold" value={health} onChange={(e) => setHealth(Number(e.target.value))} required />
                  </div>
                  <div>
                    <label className="block text-slate-500 font-bold mb-1">First Term (G1 score: 0-20)</label>
                    <input type="number" min={0} max={20} className="w-full px-3 py-2 border rounded-lg bg-white font-semibold" value={g1} onChange={(e) => setG1(Number(e.target.value))} required />
                  </div>
                  <div>
                    <label className="block text-slate-500 font-bold mb-1">Second Term (G2 score: 0-20)</label>
                    <input type="number" min={0} max={20} className="w-full px-3 py-2 border rounded-lg bg-white font-semibold" value={g2} onChange={(e) => setG2(Number(e.target.value))} required />
                  </div>
                </div>
                <div className="flex justify-end gap-2 text-xs">
                  <button type="button" onClick={() => setShowRecordForm(false)} className="px-3 py-1.5 border rounded-lg hover:bg-slate-100 text-slate-500 font-bold">Cancel</button>
                  <button type="submit" className="px-4 py-1.5 bg-blue-600 text-white rounded-lg font-bold hover:bg-blue-700" disabled={recordMutation.isPending}>Save Performance Log</button>
                </div>
              </form>
            )}

            {records.length === 0 ? (
              <p className="text-slate-400 text-sm font-semibold italic">No performance logs recorded for this student.</p>
            ) : (
              <div className="bg-white border border-slate-100 rounded-2xl overflow-hidden shadow-sm">
                <table className="w-full text-left">
                  <thead>
                    <tr className="bg-slate-50 border-b border-slate-100 text-xs font-bold text-slate-400 uppercase tracking-wider">
                      <th className="p-4">Date Logged</th>
                      <th className="p-4">Study Time</th>
                      <th className="p-4">Failures</th>
                      <th className="p-4">Absences</th>
                      <th className="p-4">Support</th>
                      <th className="p-4">G1 Grade</th>
                      <th className="p-4">G2 Grade</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100 text-xs font-semibold text-slate-600">
                    {records.map((rec) => (
                      <tr key={rec.id}>
                        <td className="p-4 font-bold text-slate-800">{new Date(rec.created_at).toLocaleDateString()}</td>
                        <td className="p-4">{rec.study_time} hrs/week</td>
                        <td className="p-4">{rec.failures}</td>
                        <td className="p-4">{rec.absences} days</td>
                        <td className="p-4">Fam: {rec.family_support} | School: {rec.school_support}</td>
                        <td className="p-4 font-bold">{rec.g1}/20</td>
                        <td className="p-4 font-bold">{rec.g2}/20</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        )}

        {/* tab 3: Multimodal file reports upload */}
        {activeTab === 'DOCUMENTS' && (
          <div className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <div>
                <h3 className="font-bold text-slate-800 text-base mb-4">Upload File</h3>
                <DocumentUploader
                  onUpload={handleUploadDocument}
                  isUploading={isUploading}
                />
              </div>

              <div className="lg:col-span-2">
                <h3 className="font-bold text-slate-800 text-base mb-4">Extracted Structured Previews</h3>
                {documents.map((doc) => (
                  <div key={doc.id} className="p-4 border rounded-2xl bg-slate-50 space-y-4 mb-4 border-slate-200">
                    <div className="flex items-center justify-between border-b pb-2 text-xs font-semibold text-slate-500">
                      <div>
                        <span className="font-bold text-slate-800">{doc.filename}</span>
                        <p className="text-[10px] text-slate-400 mt-0.5">Uploaded {new Date(doc.created_at).toLocaleString()}</p>
                      </div>
                      <span className={cn(
                        "px-2 py-0.5 border text-[9px] font-bold rounded uppercase",
                        doc.processing_status === 'COMPLETED' ? 'bg-emerald-50 text-emerald-700 border-emerald-100' :
                        (doc.processing_status === 'FAILED' ? 'bg-red-50 text-red-700 border-red-100' : 'bg-amber-50 text-amber-700 border-amber-100 animate-pulse')
                      )}>
                        {doc.processing_status}
                      </span>
                    </div>
                    {doc.processing_status === 'COMPLETED' && (
                      <ExtractedDataPreview document={doc} />
                    )}
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </PageContainer>
  );
};
