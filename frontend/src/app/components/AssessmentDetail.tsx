'use client';

import React, { useState, useEffect } from 'react';
import { Assessment, submitHitlReview, getPdfDownloadUrl, getStaticFileUrl } from '../utils/api';

interface AssessmentDetailProps {
  assessment: Assessment;
  onClose: () => void;
  onUpdate: (updated: Assessment) => void;
}

export default function AssessmentDetail({ assessment, onClose, onUpdate }: AssessmentDetailProps) {
  // HITL Form State
  const [overrideLstm, setOverrideLstm] = useState<number | ''>('');
  const [overrideCnn, setOverrideCnn] = useState<number | ''>('');
  const [overrideAnn, setOverrideAnn] = useState<number | ''>('');
  const [notes, setNotes] = useState('');
  const [analystName, setAnalystName] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [successMsg, setSuccessMsg] = useState('');

  useEffect(() => {
    // Populate form if already reviewed
    setOverrideLstm(assessment.override_lstm_class !== null && assessment.override_lstm_class !== undefined ? assessment.override_lstm_class : '');
    setOverrideCnn(assessment.override_cnn_class !== null && assessment.override_cnn_class !== undefined ? assessment.override_cnn_class : '');
    setOverrideAnn(assessment.override_ann_class !== null && assessment.override_ann_class !== undefined ? assessment.override_ann_class : '');
    setNotes(assessment.analyst_notes || '');
    setAnalystName(assessment.reviewed_by || '');
    setSuccessMsg('');
  }, [assessment]);

  const handleSaveReview = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    setSuccessMsg('');
    try {
      const updated = await submitHitlReview(assessment.id, {
        override_lstm_class: overrideLstm !== '' ? Number(overrideLstm) : undefined,
        override_cnn_class: overrideCnn !== '' ? Number(overrideCnn) : undefined,
        override_ann_class: overrideAnn !== '' ? Number(overrideAnn) : undefined,
        analyst_notes: notes,
        reviewed_by: analystName || 'Analyst',
      });
      onUpdate(updated);
      setSuccessMsg('Human-in-the-Loop verification saved & signed off successfully!');
    } catch (err: any) {
      alert(`Error saving review: ${err.message}`);
    } finally {
      setSubmitting(false);
    }
  };

  // Mappings
  const lstmLabels = ['Low Risk', 'Medium Risk', 'High Risk'];
  const cnnLabels = ['Healthy (No cracks)', 'Damaged (Cracks detected)'];
  const annLabels = ['Normal Sound', 'Anomalous Sound'];

  // Importance Colors
  const featColors: Record<string, string> = {
    temperature: 'bg-amber-500',
    vibration: 'bg-rose-500',
    pressure: 'bg-sky-500',
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm overflow-y-auto">
      <div className="relative w-full max-w-6xl bg-slate-900 border border-slate-800 rounded-2xl shadow-2xl flex flex-col max-h-[90vh] overflow-hidden">
        
        {/* Header */}
        <div className="px-6 py-4 bg-slate-950 border-b border-slate-800 flex justify-between items-center">
          <div>
            <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
              <span className="h-3 w-3 rounded-full bg-blue-500 animate-pulse"></span>
              {assessment.asset_name} Assessment
            </h2>
            <p className="text-xs text-slate-400">
              Location: {assessment.location} | ID: {assessment.id} | Analyzed on: {new Date(assessment.created_at).toLocaleString()}
            </p>
          </div>
          <button 
            onClick={onClose}
            className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white rounded-lg transition text-sm"
          >
            Close Dashboard
          </button>
        </div>

        {/* Scrollable Split-Pane Body */}
        <div className="flex-1 overflow-y-auto grid grid-cols-1 lg:grid-cols-2 divide-y lg:divide-y-0 lg:divide-x divide-slate-800">
          
          {/* Left Pane: Model Diagnostic Outputs & XAI */}
          <div className="p-6 space-y-6">
            <h3 className="text-md font-bold text-blue-400 uppercase tracking-wider border-b border-slate-800 pb-2">
              Deep Learning Diagnostics & XAI
            </h3>

            {/* 1. Tabular (LSTM) Analysis */}
            <div className="bg-slate-950/40 p-4 border border-slate-800/80 rounded-xl space-y-4">
              <div className="flex justify-between items-center">
                <span className="text-sm font-semibold text-slate-300">LSTM Time-Series Risk Predictor</span>
                <span className={`px-2 py-0.5 rounded text-xs font-bold ${
                  assessment.lstm_prediction_class === 2 ? 'bg-rose-500/20 text-rose-400 border border-rose-500/30' :
                  assessment.lstm_prediction_class === 1 ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30' :
                  'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                }`}>
                  Initial AI: {lstmLabels[assessment.lstm_prediction_class]}
                </span>
              </div>

              {/* Feature Importance (Perturbation SHAP) */}
              <div className="space-y-2">
                <span className="text-xs font-bold text-slate-400 flex justify-between">
                  <span>XAI Feature Attributions (Perturbation-based)</span>
                  <span>Impact Score %</span>
                </span>
                
                {Object.entries(assessment.lstm_feature_importance).map(([feature, val]) => (
                  <div key={feature} className="space-y-1">
                    <div className="flex justify-between text-xs text-slate-300">
                      <span className="capitalize">{feature}</span>
                      <span>{(val * 100).toFixed(1)}%</span>
                    </div>
                    <div className="h-2 w-full bg-slate-800 rounded-full overflow-hidden">
                      <div 
                        className={`h-full ${featColors[feature] || 'bg-blue-500'} rounded-full transition-all duration-500`}
                        style={{ width: `${val * 100}%` }}
                      ></div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* 2. Visual (CNN) Inspection with Grad-CAM */}
            <div className="bg-slate-950/40 p-4 border border-slate-800/80 rounded-xl space-y-4">
              <div className="flex justify-between items-center">
                <span className="text-sm font-semibold text-slate-300">CNN Visual Crack Detector</span>
                <span className={`px-2 py-0.5 rounded text-xs font-bold ${
                  assessment.cnn_prediction_class === 1 ? 'bg-rose-500/20 text-rose-400 border border-rose-500/30' :
                  'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                }`}>
                  Initial AI: {cnnLabels[assessment.cnn_prediction_class]} ({(assessment.cnn_confidence_score * 100).toFixed(1)}%)
                </span>
              </div>

              {/* Images Grid */}
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-1">
                  <span className="text-xs text-slate-400 font-semibold block text-center">Inspection Original</span>
                  <div className="aspect-square bg-slate-900 border border-slate-800 rounded-lg overflow-hidden flex items-center justify-center relative">
                    {assessment.image_path ? (
                      <img 
                        src={getStaticFileUrl(assessment.image_path)} 
                        alt="Inspection Original" 
                        className="object-cover w-full h-full"
                        onError={(e) => {
                          e.currentTarget.style.display = 'none';
                        }}
                      />
                    ) : (
                      <span className="text-xs text-slate-500">No Image</span>
                    )}
                  </div>
                </div>

                <div className="space-y-1">
                  <span className="text-xs text-slate-400 font-semibold block text-center">XAI Grad-CAM Saliency</span>
                  <div className="aspect-square bg-slate-900 border border-slate-800 rounded-lg overflow-hidden flex items-center justify-center relative">
                    {assessment.cnn_gradcam_path ? (
                      <img 
                        src={getStaticFileUrl(assessment.cnn_gradcam_path)} 
                        alt="Grad-CAM Overlay" 
                        className="object-cover w-full h-full"
                        onError={(e) => {
                          e.currentTarget.style.display = 'none';
                        }}
                      />
                    ) : (
                      <span className="text-xs text-slate-500">No Grad-CAM</span>
                    )}
                  </div>
                </div>
              </div>
            </div>

            {/* 3. Audio (ANN) Noise Diagnostics */}
            <div className="bg-slate-950/40 p-4 border border-slate-800/80 rounded-xl flex justify-between items-center">
              <div>
                <span className="text-sm font-semibold text-slate-300 block">ANN Acoustic Spectrum Diagnostic</span>
                <span className="text-xs text-slate-500">Classifies audio inspector notes or machinery acoustic hums.</span>
              </div>
              <span className={`px-2 py-1 rounded text-xs font-bold ${
                assessment.ann_prediction_class === 1 ? 'bg-rose-500/20 text-rose-400 border border-rose-500/30' :
                'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
              }`}>
                Initial AI: {annLabels[assessment.ann_prediction_class]} ({(assessment.ann_confidence_score * 100).toFixed(1)}%)
              </span>
            </div>

          </div>

          {/* Right Pane: LLM Text reports, RAG data, and Human-in-the-Loop panel */}
          <div className="p-6 space-y-6 flex flex-col h-full overflow-hidden">
            <h3 className="text-md font-bold text-teal-400 uppercase tracking-wider border-b border-slate-800 pb-2">
              Compliance report & analyst review (HITL)
            </h3>

            {/* RAG Report Content */}
            <div className="space-y-4 flex-1 overflow-y-auto pr-1">
              <div className="space-y-1">
                <span className="text-xs font-bold text-slate-400 uppercase tracking-wide">LLM Executive Summary</span>
                <p className="text-sm text-slate-300 bg-slate-950/40 border border-slate-850 p-3 rounded-lg leading-relaxed">
                  {assessment.llm_summary || 'Generating summary report...'}
                </p>
              </div>

              <div className="space-y-1">
                <span className="text-xs font-bold text-slate-400 uppercase tracking-wide">AI Risk Reasoning</span>
                <p className="text-sm text-slate-300 bg-slate-950/40 border border-slate-850 p-3 rounded-lg leading-relaxed whitespace-pre-line">
                  {assessment.llm_reasoning || 'Analyzing model parameters...'}
                </p>
              </div>

              <div className="space-y-1">
                <span className="text-xs font-bold text-slate-400 uppercase tracking-wide">Recommended Actions (RAG Compliance Guidelines)</span>
                <div className="text-sm text-slate-300 bg-slate-950/40 border border-slate-850 p-3 rounded-lg space-y-2 whitespace-pre-line leading-relaxed">
                  {assessment.llm_mitigation || 'Fetching regulatory mitigations...'}
                </div>
              </div>
            </div>

            {/* HITL Override Form */}
            <form onSubmit={handleSaveReview} className="border-t border-slate-800 pt-4 space-y-4 bg-slate-950/50 p-4 rounded-xl">
              <span className="text-xs font-bold text-slate-200 uppercase tracking-wide block">
                Human-in-the-Loop Analyst overrides
              </span>

              {successMsg && (
                <div className="p-2.5 bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 rounded-lg text-xs font-medium">
                  {successMsg}
                </div>
              )}

              {/* Overrides Selection Row */}
              <div className="grid grid-cols-3 gap-3">
                <div className="space-y-1">
                  <label className="text-[10px] font-bold text-slate-400 block uppercase">Override LSTM</label>
                  <select 
                    value={overrideLstm} 
                    onChange={(e) => setOverrideLstm(e.target.value !== '' ? Number(e.target.value) : '')}
                    className="w-full bg-slate-900 border border-slate-700 text-slate-200 rounded p-1.5 text-xs focus:ring-1 focus:ring-teal-500 focus:outline-none"
                  >
                    <option value="">Keep AI Pred</option>
                    <option value="0">Low Risk</option>
                    <option value="1">Medium Risk</option>
                    <option value="2">High Risk</option>
                  </select>
                </div>

                <div className="space-y-1">
                  <label className="text-[10px] font-bold text-slate-400 block uppercase">Override CNN</label>
                  <select 
                    value={overrideCnn} 
                    onChange={(e) => setOverrideCnn(e.target.value !== '' ? Number(e.target.value) : '')}
                    className="w-full bg-slate-900 border border-slate-700 text-slate-200 rounded p-1.5 text-xs focus:ring-1 focus:ring-teal-500 focus:outline-none"
                  >
                    <option value="">Keep AI Pred</option>
                    <option value="0">Healthy</option>
                    <option value="1">Damaged</option>
                  </select>
                </div>

                <div className="space-y-1">
                  <label className="text-[10px] font-bold text-slate-400 block uppercase">Override ANN</label>
                  <select 
                    value={overrideAnn} 
                    onChange={(e) => setOverrideAnn(e.target.value !== '' ? Number(e.target.value) : '')}
                    className="w-full bg-slate-900 border border-slate-700 text-slate-200 rounded p-1.5 text-xs focus:ring-1 focus:ring-teal-500 focus:outline-none"
                  >
                    <option value="">Keep AI Pred</option>
                    <option value="0">Normal Sound</option>
                    <option value="1">Anomalous Sound</option>
                  </select>
                </div>
              </div>

              {/* Analyst Comments */}
              <div className="space-y-1">
                <label className="text-[10px] font-bold text-slate-400 block uppercase">Analyst Inspection Remarks</label>
                <textarea
                  value={notes}
                  onChange={(e) => setNotes(e.target.value)}
                  placeholder="Type official inspection details, reasons for overrides, or verification remarks here..."
                  rows={2}
                  className="w-full bg-slate-900 border border-slate-700 text-slate-200 rounded p-2 text-xs focus:ring-1 focus:ring-teal-500 focus:outline-none placeholder-slate-600 resize-none"
                />
              </div>

              {/* Actions row */}
              <div className="flex gap-3 items-center">
                <div className="flex-1 space-y-1">
                  <input
                    type="text"
                    value={analystName}
                    onChange={(e) => setAnalystName(e.target.value)}
                    placeholder="Analyst Name / Signature"
                    required
                    className="w-full bg-slate-900 border border-slate-700 text-slate-200 rounded p-2 text-xs focus:ring-1 focus:ring-teal-500 focus:outline-none placeholder-slate-600"
                  />
                </div>

                <button
                  type="submit"
                  disabled={submitting}
                  className="px-4 py-2 bg-gradient-to-r from-teal-500 to-cyan-500 hover:from-teal-600 hover:to-cyan-600 text-slate-950 font-bold rounded-lg text-xs transition duration-200 disabled:opacity-50"
                >
                  {submitting ? 'Signing off...' : 'Sign-off & Approve'}
                </button>

                <a
                  href={getPdfDownloadUrl(assessment.id)}
                  target="_blank"
                  rel="noreferrer"
                  className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-teal-400 hover:text-teal-300 font-bold rounded-lg text-xs transition duration-200 text-center"
                >
                  Download PDF
                </a>
              </div>
            </form>

          </div>

        </div>

      </div>
    </div>
  );
}
