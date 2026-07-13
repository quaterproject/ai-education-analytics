'use client';

import React, { useState, useEffect } from 'react';
import { fetchAssessments, createAssessment, Assessment } from './utils/api';
import AssessmentDetail from './components/AssessmentDetail';

export default function Home() {
  const [assessments, setAssessments] = useState<Assessment[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedAssessment, setSelectedAssessment] = useState<Assessment | null>(null);
  
  // Upload Form State
  const [assetName, setAssetName] = useState('');
  const [location, setLocation] = useState('');
  const [description, setDescription] = useState('');
  
  const [sensorCsv, setSensorCsv] = useState<File | null>(null);
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [audioFile, setAudioFile] = useState<File | null>(null);
  const [complianceDoc, setComplianceDoc] = useState<File | null>(null);
  
  const [runningInference, setRunningInference] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  // Fetch initial assessments
  const loadData = async () => {
    try {
      const data = await fetchAssessments();
      setAssessments(data);
    } catch (err) {
      console.error('Error fetching assessments:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleInspectSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!assetName || !location) {
      alert('Please fill out Asset Name and Location fields.');
      return;
    }
    setRunningInference(true);
    
    const formData = new FormData();
    formData.append('asset_name', assetName);
    formData.append('location', location);
    if (description) formData.append('description', description);
    
    if (sensorCsv) formData.append('sensor_csv', sensorCsv);
    if (imageFile) formData.append('image_file', imageFile);
    if (audioFile) formData.append('audio_file', audioFile);
    if (complianceDoc) formData.append('compliance_doc', complianceDoc);

    try {
      const newAssessment = await createAssessment(formData);
      setAssessments((prev) => [newAssessment, ...prev]);
      
      // Clear inputs
      setAssetName('');
      setLocation('');
      setDescription('');
      setSensorCsv(null);
      setImageFile(null);
      setAudioFile(null);
      setComplianceDoc(null);
      
      // Open the detail page for the newly created assessment immediately!
      setSelectedAssessment(newAssessment);
    } catch (err: any) {
      alert(`Diagnostic Pipeline failed: ${err.message}`);
    } finally {
      setRunningInference(false);
    }
  };

  const updateAssessment = (updated: Assessment) => {
    setAssessments((prev) =>
      prev.map((item) => (item.id === updated.id ? updated : item))
    );
    if (selectedAssessment?.id === updated.id) {
      setSelectedAssessment(updated);
    }
  };

  // Filtered list
  const filteredAssessments = assessments.filter(
    (item) =>
      item.asset_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      item.location.toLowerCase().includes(searchQuery.toLowerCase())
  );

  // Statistics calculation
  const totalAssets = assessments.length;
  
  const highRiskCount = assessments.filter((item) => {
    const finalRisk = item.override_lstm_class !== null && item.override_lstm_class !== undefined
      ? item.override_lstm_class
      : item.lstm_prediction_class;
    return finalRisk === 2;
  }).length;

  const pendingVerificationCount = assessments.filter((item) => !item.is_reviewed).length;
  
  const healthRate = totalAssets > 0 
    ? Math.round(((totalAssets - assessments.filter((item) => {
        const finalDamage = item.override_cnn_class !== null && item.override_cnn_class !== undefined
          ? item.override_cnn_class
          : item.cnn_prediction_class;
        return finalDamage === 1;
      }).length) / totalAssets) * 100)
    : 100;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans selection:bg-teal-500/20 selection:text-teal-400">
      
      {/* Navbar */}
      <header className="border-b border-slate-900 bg-slate-950/80 backdrop-blur-md sticky top-0 z-40 px-6 py-4 flex justify-between items-center">
        <div className="flex items-center gap-2.5">
          <div className="h-9 w-9 rounded-xl bg-gradient-to-tr from-teal-500 to-indigo-500 flex items-center justify-center font-bold text-slate-950 text-lg shadow-lg shadow-teal-500/10">
            Ω
          </div>
          <div>
            <h1 className="font-extrabold text-md tracking-tight text-white flex items-center gap-2">
              OMNIRISK AI <span className="text-[10px] font-bold px-1.5 py-0.5 rounded bg-teal-500/10 text-teal-400 border border-teal-500/20">PRO</span>
            </h1>
            <p className="text-[10px] text-slate-400 font-semibold tracking-wider uppercase">Multimodal Asset Safety & Compliance</p>
          </div>
        </div>

        <div className="flex items-center gap-4 text-xs font-bold text-slate-400">
          <span className="flex items-center gap-1.5 bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 px-2.5 py-1 rounded-full">
            <span className="h-1.5 w-1.5 bg-emerald-500 rounded-full animate-pulse"></span>
            NEON DATABASE ACTIVE
          </span>
          <span className="flex items-center gap-1.5 bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 px-2.5 py-1 rounded-full">
            <span className="h-1.5 w-1.5 bg-indigo-500 rounded-full animate-pulse"></span>
            QDRANT VECTOR DB
          </span>
        </div>
      </header>

      {/* Main Panel */}
      <main className="flex-1 max-w-7xl w-full mx-auto p-6 space-y-6">
        
        {/* Statistics Cards */}
        <section className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="p-4 bg-slate-900 border border-slate-800 rounded-xl flex items-center justify-between shadow-md">
            <div>
              <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">Inspected Assets</span>
              <span className="text-2xl font-black text-slate-100">{totalAssets}</span>
            </div>
            <span className="text-xl">🏭</span>
          </div>

          <div className="p-4 bg-slate-900 border border-slate-800 rounded-xl flex items-center justify-between shadow-md">
            <div>
              <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">Critical High-Risk</span>
              <span className="text-2xl font-black text-rose-500">{highRiskCount}</span>
            </div>
            <span className="text-xl">⚠️</span>
          </div>

          <div className="p-4 bg-slate-900 border border-slate-800 rounded-xl flex items-center justify-between shadow-md">
            <div>
              <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">Pending Analyst Review</span>
              <span className="text-2xl font-black text-amber-500">{pendingVerificationCount}</span>
            </div>
            <span className="text-xl">⏱️</span>
          </div>

          <div className="p-4 bg-slate-900 border border-slate-800 rounded-xl flex items-center justify-between shadow-md">
            <div>
              <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">Visual Health Rate</span>
              <span className="text-2xl font-black text-emerald-500">{healthRate}%</span>
            </div>
            <span className="text-xl">🛡️</span>
          </div>
        </section>

        {/* Dashboard Split Column: Left=Upload Inspector Form, Right=Assessments List */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 items-start">
          
          {/* Upload Form Box */}
          <section className="bg-slate-900 border border-slate-800 p-5 rounded-2xl shadow-xl space-y-4 lg:col-span-1">
            <div className="border-b border-slate-800 pb-3">
              <h2 className="text-md font-bold text-slate-100 flex items-center gap-1.5">
                <span>➕</span> Inspect New Asset
              </h2>
              <p className="text-xs text-slate-400 mt-1">Upload multimodal inspection readings to trigger deep learning analysis, XAI maps, and RAG compliance reporting.</p>
            </div>

            <form onSubmit={handleInspectSubmit} className="space-y-4 text-sm">
              <div className="space-y-1">
                <label className="text-[10px] font-bold text-slate-400 uppercase">Asset Name</label>
                <input
                  type="text"
                  value={assetName}
                  onChange={(e) => setAssetName(e.target.value)}
                  placeholder="e.g. Electric Turbine G-4"
                  required
                  className="w-full bg-slate-950 border border-slate-800 text-slate-200 rounded-lg p-2.5 text-xs focus:ring-1 focus:ring-teal-500 focus:outline-none placeholder-slate-700"
                />
              </div>

              <div className="space-y-1">
                <label className="text-[10px] font-bold text-slate-400 uppercase">Location / Sector</label>
                <input
                  type="text"
                  value={location}
                  onChange={(e) => setLocation(e.target.value)}
                  placeholder="e.g. Sector 4 - Plant B"
                  required
                  className="w-full bg-slate-950 border border-slate-800 text-slate-200 rounded-lg p-2.5 text-xs focus:ring-1 focus:ring-teal-500 focus:outline-none placeholder-slate-700"
                />
              </div>

              <div className="space-y-1">
                <label className="text-[10px] font-bold text-slate-400 uppercase">Description</label>
                <textarea
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  placeholder="Operational comments..."
                  rows={2}
                  className="w-full bg-slate-950 border border-slate-800 text-slate-200 rounded-lg p-2.5 text-xs focus:ring-1 focus:ring-teal-500 focus:outline-none placeholder-slate-700 resize-none"
                />
              </div>

              {/* Multimodal Inputs */}
              <div className="space-y-3 pt-2 border-t border-slate-800">
                <span className="text-[10px] font-black text-teal-400 uppercase block tracking-wider">Inspector Reading Uploads</span>

                {/* Tabular CSV */}
                <div className="space-y-1">
                  <label className="text-[10px] font-bold text-slate-400 flex justify-between">
                    <span>1. Tabular Time-Series (CSV)</span>
                    <span className="text-slate-600">e.g. temp,vib,pressure</span>
                  </label>
                  <input
                    type="file"
                    accept=".csv"
                    onChange={(e) => setSensorCsv(e.target.files ? e.target.files[0] : null)}
                    className="w-full bg-slate-950 border border-slate-800 text-slate-400 text-xs rounded-lg file:mr-3 file:py-1 file:px-2.5 file:rounded-md file:border-0 file:text-[10px] file:font-extrabold file:bg-slate-800 file:text-slate-300 file:cursor-pointer cursor-pointer hover:file:bg-slate-700 p-1"
                  />
                </div>

                {/* CNN Image */}
                <div className="space-y-1">
                  <label className="text-[10px] font-bold text-slate-400">2. Visual Inspection Image (JPG/PNG)</label>
                  <input
                    type="file"
                    accept="image/*"
                    onChange={(e) => setImageFile(e.target.files ? e.target.files[0] : null)}
                    className="w-full bg-slate-950 border border-slate-800 text-slate-400 text-xs rounded-lg file:mr-3 file:py-1 file:px-2.5 file:rounded-md file:border-0 file:text-[10px] file:font-extrabold file:bg-slate-800 file:text-slate-300 file:cursor-pointer cursor-pointer hover:file:bg-slate-700 p-1"
                  />
                </div>

                {/* Audio WAV */}
                <div className="space-y-1">
                  <label className="text-[10px] font-bold text-slate-400">3. Acoustic Machinery Noise (WAV)</label>
                  <input
                    type="file"
                    accept="audio/wav,audio/*"
                    onChange={(e) => setAudioFile(e.target.files ? e.target.files[0] : null)}
                    className="w-full bg-slate-950 border border-slate-800 text-slate-400 text-xs rounded-lg file:mr-3 file:py-1 file:px-2.5 file:rounded-md file:border-0 file:text-[10px] file:font-extrabold file:bg-slate-800 file:text-slate-300 file:cursor-pointer cursor-pointer hover:file:bg-slate-700 p-1"
                  />
                </div>

                {/* Compliance Regulation RAG PDF */}
                <div className="space-y-1">
                  <label className="text-[10px] font-bold text-indigo-400">4. Dynamic RAG Regulations (PDF/TXT)</label>
                  <input
                    type="file"
                    accept=".pdf,.txt"
                    onChange={(e) => setComplianceDoc(e.target.files ? e.target.files[0] : null)}
                    className="w-full bg-slate-950 border border-slate-800 text-slate-400 text-xs rounded-lg file:mr-3 file:py-1 file:px-2.5 file:rounded-md file:border-0 file:text-[10px] file:font-extrabold file:bg-slate-800 file:text-slate-300 file:cursor-pointer cursor-pointer hover:file:bg-slate-700 p-1"
                  />
                </div>
              </div>

              {/* Submit Diagnostics */}
              <button
                type="submit"
                disabled={runningInference}
                className="w-full py-2.5 bg-gradient-to-r from-teal-500 to-indigo-500 hover:from-teal-600 hover:to-indigo-600 text-slate-950 font-black rounded-xl transition duration-200 shadow-lg shadow-teal-500/5 disabled:opacity-50 text-xs uppercase"
              >
                {runningInference ? 'Running Pipeline Models...' : 'Run Diagnostics'}
              </button>
            </form>
          </section>

          {/* List panel */}
          <section className="bg-slate-900 border border-slate-800 p-5 rounded-2xl shadow-xl space-y-4 lg:col-span-2">
            <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-3 border-b border-slate-800 pb-3">
              <div>
                <h2 className="text-md font-bold text-slate-100 flex items-center gap-1.5">
                  <span>📊</span> Diagnostic Assessment Queue
                </h2>
                <p className="text-xs text-slate-400 mt-1">Review AI predictions and sign off final assessments.</p>
              </div>

              {/* Search filter */}
              <input
                type="text"
                placeholder="Search asset or location..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="bg-slate-950 border border-slate-800 text-slate-300 rounded-lg px-3 py-1.5 text-xs focus:ring-1 focus:ring-teal-500 focus:outline-none placeholder-slate-700 w-full sm:w-60"
              />
            </div>

            {loading ? (
              <div className="py-16 text-center text-xs text-slate-500 font-semibold uppercase animate-pulse">
                Fetching assessments from Neon Database...
              </div>
            ) : filteredAssessments.length === 0 ? (
              <div className="py-16 text-center text-xs text-slate-500 font-semibold">
                No inspection assessments found. Add one on the left to start!
              </div>
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs border-collapse">
                  <thead>
                    <tr className="border-b border-slate-800 text-slate-400 uppercase tracking-wider text-[10px] font-black">
                      <th className="py-2.5 px-3">Asset Details</th>
                      <th className="py-2.5 px-3">Location</th>
                      <th className="py-2.5 px-3 text-center">LSTM Risk</th>
                      <th className="py-2.5 px-3 text-center">CNN Visual</th>
                      <th className="py-2.5 px-3 text-center">ANN Audio</th>
                      <th className="py-2.5 px-3 text-right">Sign-off Status</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800/60">
                    {filteredAssessments.map((item) => {
                      const finalLstm = item.override_lstm_class !== null && item.override_lstm_class !== undefined ? item.override_lstm_class : item.lstm_prediction_class;
                      const finalCnn = item.override_cnn_class !== null && item.override_cnn_class !== undefined ? item.override_cnn_class : item.cnn_prediction_class;
                      const finalAnn = item.override_ann_class !== null && item.override_ann_class !== undefined ? item.override_ann_class : item.ann_prediction_class;
                      
                      const lstmRiskText = ['Low', 'Medium', 'High'];
                      const cnnDamageText = ['Healthy', 'Damaged'];
                      const annAudioText = ['Normal', 'Anomaly'];

                      return (
                        <tr
                          key={item.id}
                          onClick={() => setSelectedAssessment(item)}
                          className="hover:bg-slate-800/40 cursor-pointer transition duration-150"
                        >
                          <td className="py-3 px-3">
                            <span className="font-bold text-slate-200 block">{item.asset_name}</span>
                            <span className="text-[10px] text-slate-500">{new Date(item.created_at).toLocaleDateString()}</span>
                          </td>
                          <td className="py-3 px-3 text-slate-400">{item.location}</td>
                          <td className="py-3 px-3 text-center">
                            <span className={`px-2 py-0.5 rounded-full text-[10px] font-black ${
                              finalLstm === 2 ? 'bg-rose-500/10 text-rose-400 border border-rose-500/20' :
                              finalLstm === 1 ? 'bg-amber-500/10 text-amber-400 border border-amber-500/20' :
                              'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                            }`}>
                              {lstmRiskText[finalLstm]}
                            </span>
                          </td>
                          <td className="py-3 px-3 text-center">
                            <span className={`px-2 py-0.5 rounded-full text-[10px] font-black ${
                              finalCnn === 1 ? 'bg-rose-500/10 text-rose-400 border border-rose-500/20' :
                              'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                            }`}>
                              {cnnDamageText[finalCnn]}
                            </span>
                          </td>
                          <td className="py-3 px-3 text-center">
                            <span className={`px-2 py-0.5 rounded-full text-[10px] font-black ${
                              finalAnn === 1 ? 'bg-rose-500/10 text-rose-400 border border-rose-500/20' :
                              'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                            }`}>
                              {annAudioText[finalAnn]}
                            </span>
                          </td>
                          <td className="py-3 px-3 text-right">
                            <span className={`px-2 py-0.5 rounded text-[10px] font-extrabold ${
                              item.is_reviewed 
                                ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' 
                                : 'bg-slate-800 text-slate-400'
                            }`}>
                              {item.is_reviewed ? 'SIGNED OFF' : 'UNREVIEWED'}
                            </span>
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            )}
          </section>

        </div>

      </main>

      {/* Detail Overlay Modal */}
      {selectedAssessment && (
        <AssessmentDetail
          assessment={selectedAssessment}
          onClose={() => setSelectedAssessment(null)}
          onUpdate={updateAssessment}
        />
      )}

      {/* Footer */}
      <footer className="border-t border-slate-900 bg-slate-950 py-4 px-6 text-center text-[10px] text-slate-600 font-semibold mt-auto">
        &copy; {new Date().getFullYear()} OMNIRISK AI INC. ALL RIGHTS RESERVED. CERTIFIED SYSTEM ASSESSMENT SECURED BY NEON POSTGRESQL.
      </footer>

    </div>
  );
}
