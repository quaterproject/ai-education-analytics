import os
import json
import uuid
import numpy as np
import tensorflow as tf
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, Depends, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

# Import backend modules
from src.api.db import get_db, init_db, AssetAssessment
from src.api.rag import index_document, generate_report
from src.api.pdf_generator import generate_pdf_report
from src.models.xai import generate_gradcam, generate_perturbation_importance

# Create directories
os.makedirs("data/uploads", exist_ok=True)
os.makedirs("data/models", exist_ok=True)
os.makedirs("data/samples", exist_ok=True)

# Initialize database
init_db()

app = FastAPI(title="OmniRisk AI - Multimodal Inspection Backend")

# CORS middleware to allow next.js requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount uploads and samples directories to serve static images/Grad-CAM overlays
app.mount("/data", StaticFiles(directory="data"), name="data")

# Helper function to extract audio features from WAV
def extract_audio_features(file_path: str) -> np.ndarray:
    import wave
    try:
        with wave.open(file_path, 'rb') as wav:
            n_frames = wav.getnframes()
            frames = wav.readframes(n_frames)
            audio_data = np.frombuffer(frames, dtype=np.int16)
            audio_data = audio_data.astype(np.float32) / 32768.0
            
            # Extract 13 energy bands
            if len(audio_data) < 13:
                # pad if too short
                audio_data = np.pad(audio_data, (0, 13 - len(audio_data)), 'constant')
                
            segment_len = len(audio_data) // 13
            features = []
            for i in range(13):
                segment = audio_data[i * segment_len : (i + 1) * segment_len]
                if len(segment) > 0:
                    features.append(float(np.sqrt(np.mean(segment**2))))
                else:
                    features.append(0.0)
            
            features = np.array(features)
            max_f = np.max(features)
            if max_f > 0:
                features = features / max_f
            return features
    except Exception as e:
        print(f"Error parsing audio wave file: {e}. Using random mock features.")
        return np.random.rand(13).astype(np.float32)

@app.get("/")
def read_root():
    return {"message": "OmniRisk AI Backend running successfully!"}

@app.post("/api/assessments")
async def create_assessment(
    asset_name: str = Form(...),
    location: str = Form(...),
    description: Optional[str] = Form(None),
    sensor_csv: Optional[UploadFile] = File(None),
    image_file: Optional[UploadFile] = File(None),
    audio_file: Optional[UploadFile] = File(None),
    compliance_doc: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    try:
        # Generate paths
        assessment_id = str(uuid.uuid4())[:8]
        
        saved_csv_path = None
        saved_img_path = None
        saved_audio_path = None
        
        # 1. Save uploaded files
        if sensor_csv:
            saved_csv_path = f"data/uploads/{assessment_id}_sensor.csv"
            with open(saved_csv_path, "wb") as f:
                f.write(await sensor_csv.read())
        else:
            # Fallback to sample
            saved_csv_path = "data/samples/sample_sensor_data.csv"
            
        if image_file:
            ext = os.path.splitext(image_file.filename)[1] or ".png"
            saved_img_path = f"data/uploads/{assessment_id}_image{ext}"
            with open(saved_img_path, "wb") as f:
                f.write(await image_file.read())
        else:
            # Fallback to sample
            saved_img_path = "data/samples/sample_damaged.png"
            
        if audio_file:
            ext = os.path.splitext(audio_file.filename)[1] or ".wav"
            saved_audio_path = f"data/uploads/{assessment_id}_audio{ext}"
            with open(saved_audio_path, "wb") as f:
                f.write(await audio_file.read())
        else:
            # Fallback to sample
            saved_audio_path = "data/samples/sample_audio_features.csv"

        # 2. Index compliance documents if uploaded
        if compliance_doc:
            doc_ext = os.path.splitext(compliance_doc.filename)[1] or ".pdf"
            saved_doc_path = f"data/uploads/{assessment_id}_compliance{doc_ext}"
            with open(saved_doc_path, "wb") as f:
                f.write(await compliance_doc.read())
            # Index document in Qdrant
            try:
                index_document(saved_doc_path)
            except Exception as e:
                print(f"Error indexing compliance doc: {e}")

        # 3. Model Inference (LSTM Tabular)
        lstm_model_path = "data/models/lstm_risk_model.h5"
        if not os.path.exists(lstm_model_path):
            raise HTTPException(status_code=500, detail="LSTM model not trained. Please run training script first.")
            
        # Run XAI and predict for LSTM
        lstm_importance, lstm_class, lstm_preds = generate_perturbation_importance(lstm_model_path, saved_csv_path)

        # 4. Model Inference (CNN Image)
        cnn_model_path = "data/models/cnn_damage_model.h5"
        if not os.path.exists(cnn_model_path):
            raise HTTPException(status_code=500, detail="CNN model not trained.")
            
        # Generate Grad-CAM output overlay
        gradcam_output_path = f"data/uploads/{assessment_id}_gradcam.png"
        cnn_confidence, cnn_class = generate_gradcam(cnn_model_path, saved_img_path, gradcam_output_path)

        # 5. Model Inference (ANN Audio)
        ann_model_path = "data/models/ann_audio_model.h5"
        if not os.path.exists(ann_model_path):
            raise HTTPException(status_code=500, detail="ANN model not trained.")
            
        # Feature extraction
        if audio_file and saved_audio_path.lower().endswith(".wav"):
            audio_feats = extract_audio_features(saved_audio_path)
        else:
            # Load from CSV sample
            try:
                feats_csv = np.loadtxt(saved_audio_path, delimiter=",", skiprows=1)
                # Take first row
                if len(feats_csv.shape) > 1:
                    audio_feats = feats_csv[1] # Use anomalous one
                else:
                    audio_feats = feats_csv
            except Exception:
                audio_feats = np.random.rand(13).astype(np.float32)
                
        ann_model = tf.keras.models.load_model(ann_model_path)
        ann_preds = ann_model.predict(np.expand_dims(audio_feats, axis=0))[0]
        ann_class = int(np.argmax(ann_preds))
        ann_confidence = float(ann_preds[ann_class])

        # 6. RAG Report Generation
        report = generate_report(
            asset_name=asset_name,
            location=location,
            lstm_class=lstm_class,
            lstm_importance=lstm_importance,
            cnn_class=cnn_class,
            cnn_conf=cnn_confidence,
            ann_class=ann_class
        )

        # 7. Write to PostgreSQL Database
        assessment = AssetAssessment(
            asset_name=asset_name,
            location=location,
            description=description,
            sensor_csv_path=saved_csv_path,
            image_path=saved_img_path,
            audio_path=saved_audio_path,
            lstm_prediction_class=lstm_class,
            lstm_confidence_scores=json.dumps([float(v) for v in lstm_preds]),
            lstm_feature_importance=json.dumps(lstm_importance),
            cnn_prediction_class=cnn_class,
            cnn_confidence_score=cnn_confidence,
            cnn_gradcam_path=gradcam_output_path,
            ann_prediction_class=ann_class,
            ann_confidence_score=ann_confidence,
            llm_summary=report.get("summary"),
            llm_reasoning=report.get("reasoning"),
            llm_mitigation=report.get("mitigation"),
            is_reviewed=False
        )

        db.add(assessment)
        db.commit()
        db.refresh(assessment)

        return assessment.to_dict()

    except Exception as e:
        print(f"Error creating assessment: {e}")
        raise HTTPException(status_code=500, detail=f"Inference pipeline failed: {str(e)}")


@app.get("/api/assessments")
def list_assessments(db: Session = Depends(get_db)):
    assessments = db.query(AssetAssessment).order_by(AssetAssessment.created_at.desc()).all()
    return [a.to_dict() for a in assessments]


@app.get("/api/assessments/{assessment_id}")
def get_assessment(assessment_id: int, db: Session = Depends(get_db)):
    assessment = db.query(AssetAssessment).filter(AssetAssessment.id == assessment_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    return assessment.to_dict()


# Human-In-The-Loop (HITL) Override Endpoint
@app.post("/api/assessments/{assessment_id}/hitl")
async def submit_hitl_review(
    assessment_id: int,
    override_lstm_class: Optional[int] = Form(None),
    override_cnn_class: Optional[int] = Form(None),
    override_ann_class: Optional[int] = Form(None),
    analyst_notes: Optional[str] = Form(None),
    reviewed_by: Optional[str] = Form("Analyst"),
    db: Session = Depends(get_db)
):
    assessment = db.query(AssetAssessment).filter(AssetAssessment.id == assessment_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    assessment.is_reviewed = True
    assessment.reviewed_by = reviewed_by
    assessment.reviewed_at = datetime.utcnow()
    
    if override_lstm_class is not None:
        assessment.override_lstm_class = override_lstm_class
    if override_cnn_class is not None:
        assessment.override_cnn_class = override_cnn_class
    if override_ann_class is not None:
        assessment.override_ann_class = override_ann_class
        
    if analyst_notes is not None:
        assessment.analyst_notes = analyst_notes

    db.commit()
    db.refresh(assessment)
    return assessment.to_dict()


# Download PDF Endpoint
@app.get("/api/assessments/{assessment_id}/pdf")
def download_pdf(assessment_id: int, db: Session = Depends(get_db)):
    assessment = db.query(AssetAssessment).filter(AssetAssessment.id == assessment_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    pdf_path = f"data/uploads/report_{assessment_id}.pdf"
    
    try:
        generate_pdf_report(assessment.to_dict(), pdf_path)
        return FileResponse(
            path=pdf_path,
            filename=f"OmniRisk_Report_{assessment.asset_name.replace(' ', '_')}_{assessment_id}.pdf",
            media_type="application/pdf"
        )
    except Exception as e:
        print(f"Error compiling PDF: {e}")
        raise HTTPException(status_code=500, detail=f"PDF compilation failed: {str(e)}")
