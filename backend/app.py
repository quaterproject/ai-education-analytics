import os
import json
import numpy as np
import pandas as pd
import streamlit as st
import tensorflow as tf
from datetime import datetime

# ---- Same backend modules used by the original FastAPI app ----
from src.api.db import get_db, init_db, AssetAssessment
from src.api.rag import index_document, generate_report
from src.api.pdf_generator import generate_pdf_report
from src.models.xai import generate_gradcam, generate_perturbation_importance

# ------------------------------------------------------------------
# Setup
# ------------------------------------------------------------------
st.set_page_config(page_title="OmniRisk AI", page_icon="🛰️", layout="wide")

os.makedirs("data/uploads", exist_ok=True)
os.makedirs("data/models", exist_ok=True)
os.makedirs("data/samples", exist_ok=True)

init_db()

LSTM_MODEL_PATH = "data/models/lstm_risk_model.h5"
CNN_MODEL_PATH = "data/models/cnn_damage_model.h5"
ANN_MODEL_PATH = "data/models/ann_audio_model.h5"


def get_session():
    """get_db() in the original code is a FastAPI dependency (generator).
    Grab a plain session out of it for direct use in Streamlit."""
    return next(get_db())


def extract_audio_features(file_path: str) -> np.ndarray:
    import wave
    try:
        with wave.open(file_path, "rb") as wav:
            n_frames = wav.getnframes()
            frames = wav.readframes(n_frames)
            audio_data = np.frombuffer(frames, dtype=np.int16)
            audio_data = audio_data.astype(np.float32) / 32768.0

            if len(audio_data) < 13:
                audio_data = np.pad(audio_data, (0, 13 - len(audio_data)), "constant")

            segment_len = len(audio_data) // 13
            features = []
            for i in range(13):
                segment = audio_data[i * segment_len:(i + 1) * segment_len]
                if len(segment) > 0:
                    features.append(float(np.sqrt(np.mean(segment ** 2))))
                else:
                    features.append(0.0)

            features = np.array(features)
            max_f = np.max(features)
            if max_f > 0:
                features = features / max_f
            return features
    except Exception as e:
        st.warning(f"Error parsing audio wave file: {e}. Using random mock features.")
        return np.random.rand(13).astype(np.float32)


def save_upload(uploaded_file, path: str):
    with open(path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return path


# ------------------------------------------------------------------
# Core pipeline (mirrors POST /api/assessments from the FastAPI backend)
# ------------------------------------------------------------------
def run_assessment_pipeline(asset_name, location, description,
                             sensor_csv, image_file, audio_file, compliance_doc):
    db = get_session()
    try:
        assessment_id = str(uuid_short())

        # 1. Save uploaded files (or fall back to bundled samples)
        if sensor_csv is not None:
            saved_csv_path = save_upload(sensor_csv, f"data/uploads/{assessment_id}_sensor.csv")
        else:
            saved_csv_path = "data/samples/sample_sensor_data.csv"

        if image_file is not None:
            ext = os.path.splitext(image_file.name)[1] or ".png"
            saved_img_path = save_upload(image_file, f"data/uploads/{assessment_id}_image{ext}")
        else:
            saved_img_path = "data/samples/sample_damaged.png"

        if audio_file is not None:
            ext = os.path.splitext(audio_file.name)[1] or ".wav"
            saved_audio_path = save_upload(audio_file, f"data/uploads/{assessment_id}_audio{ext}")
        else:
            saved_audio_path = "data/samples/sample_audio_features.csv"

        # 2. Index compliance document into the Qdrant RAG store
        if compliance_doc is not None:
            doc_ext = os.path.splitext(compliance_doc.name)[1] or ".pdf"
            saved_doc_path = save_upload(compliance_doc, f"data/uploads/{assessment_id}_compliance{doc_ext}")
            try:
                index_document(saved_doc_path)
            except Exception as e:
                st.warning(f"Error indexing compliance doc: {e}")

        # 3. LSTM (tabular sensor data)
        if not os.path.exists(LSTM_MODEL_PATH):
            raise RuntimeError("LSTM model not trained. Please run training script first.")
        lstm_importance, lstm_class, lstm_preds = generate_perturbation_importance(LSTM_MODEL_PATH, saved_csv_path)

        # 4. CNN (image) + Grad-CAM
        if not os.path.exists(CNN_MODEL_PATH):
            raise RuntimeError("CNN model not trained.")
        gradcam_output_path = f"data/uploads/{assessment_id}_gradcam.png"
        cnn_confidence, cnn_class = generate_gradcam(CNN_MODEL_PATH, saved_img_path, gradcam_output_path)

        # 5. ANN (audio)
        if not os.path.exists(ANN_MODEL_PATH):
            raise RuntimeError("ANN model not trained.")
        if audio_file is not None and saved_audio_path.lower().endswith(".wav"):
            audio_feats = extract_audio_features(saved_audio_path)
        else:
            try:
                feats_csv = np.loadtxt(saved_audio_path, delimiter=",", skiprows=1)
                audio_feats = feats_csv[1] if len(feats_csv.shape) > 1 else feats_csv
            except Exception:
                audio_feats = np.random.rand(13).astype(np.float32)

        ann_model = tf.keras.models.load_model(ANN_MODEL_PATH)
        ann_preds = ann_model.predict(np.expand_dims(audio_feats, axis=0))[0]
        ann_class = int(np.argmax(ann_preds))
        ann_confidence = float(ann_preds[ann_class])

        # 6. RAG report (Qdrant retrieval + Groq LLM synthesis)
        report = generate_report(
            asset_name=asset_name,
            location=location,
            lstm_class=lstm_class,
            lstm_importance=lstm_importance,
            cnn_class=cnn_class,
            cnn_conf=cnn_confidence,
            ann_class=ann_class,
        )

        # 7. Persist to Postgres
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
            is_reviewed=False,
        )
        db.add(assessment)
        db.commit()
        db.refresh(assessment)
        return assessment.to_dict()
    finally:
        db.close()


def uuid_short():
    import uuid
    return str(uuid.uuid4())[:8]


# ------------------------------------------------------------------
# Sidebar navigation
# ------------------------------------------------------------------
st.sidebar.title("🛰️ OmniRisk AI")
page = st.sidebar.radio("Navigate", ["New Assessment", "All Assessments"])

# ------------------------------------------------------------------
# Page: New Assessment  (mirrors POST /api/assessments)
# ------------------------------------------------------------------
if page == "New Assessment":
    st.title("New Asset Assessment")
    st.caption("Upload sensor, imagery, audio and compliance data to run the multimodal risk pipeline.")

    with st.form("assessment_form", clear_on_submit=False):
        col1, col2 = st.columns(2)
        with col1:
            asset_name = st.text_input("Asset name *")
            location = st.text_input("Location *")
        with col2:
            description = st.text_area("Description", height=100)

        st.markdown("#### Multimodal inputs (optional — falls back to bundled samples)")
        c1, c2 = st.columns(2)
        with c1:
            sensor_csv = st.file_uploader("Sensor time-series (CSV)", type=["csv"])
            image_file = st.file_uploader("Structural photo", type=["png", "jpg", "jpeg"])
        with c2:
            audio_file = st.file_uploader("Machinery audio (WAV) or feature CSV", type=["wav", "csv"])
            compliance_doc = st.file_uploader("Compliance document (PDF)", type=["pdf"])

        submitted = st.form_submit_button("Run Inference Pipeline", type="primary")

    if submitted:
        if not asset_name or not location:
            st.error("Asset name and location are required.")
        else:
            with st.spinner("Running LSTM / CNN / ANN inference, XAI diagnostics and RAG report generation..."):
                try:
                    result = run_assessment_pipeline(
                        asset_name, location, description,
                        sensor_csv, image_file, audio_file, compliance_doc,
                    )
                    st.success(f"Assessment #{result['id']} created.")

                    m1, m2, m3 = st.columns(3)
                    m1.metric("LSTM Risk Class", result["lstm_prediction_class"])
                    m2.metric("CNN Damage Class", f"{result['cnn_prediction_class']} ({result['cnn_confidence_score']:.2f})")
                    m3.metric("ANN Audio Class", result["ann_prediction_class"])

                    if result.get("cnn_gradcam_path") and os.path.exists(result["cnn_gradcam_path"]):
                        st.subheader("Grad-CAM Overlay")
                        st.image(result["cnn_gradcam_path"], use_column_width=True)

                    if result.get("lstm_feature_importance"):
                        st.subheader("Tabular Feature Importance (perturbation-based)")
                        importance = json.loads(result["lstm_feature_importance"]) \
                            if isinstance(result["lstm_feature_importance"], str) else result["lstm_feature_importance"]
                        st.bar_chart(pd.Series(importance))

                    st.subheader("AI-Generated Report (RAG + Groq LLM)")
                    st.markdown(f"**Summary:** {result.get('llm_summary', '')}")
                    st.markdown(f"**Reasoning:** {result.get('llm_reasoning', '')}")
                    st.markdown(f"**Mitigation:** {result.get('llm_mitigation', '')}")

                except Exception as e:
                    st.error(f"Inference pipeline failed: {e}")

# ------------------------------------------------------------------
# Page: All Assessments  (mirrors GET /api/assessments, HITL, PDF endpoints)
# ------------------------------------------------------------------
else:
    st.title("All Assessments")
    db = get_session()
    try:
        assessments = db.query(AssetAssessment).order_by(AssetAssessment.created_at.desc()).all()
    finally:
        db.close()

    if not assessments:
        st.info("No assessments yet. Create one from the 'New Assessment' page.")
    else:
        for a in assessments:
            data = a.to_dict()
            with st.expander(f"#{data['id']} — {data['asset_name']} ({data['location']}) "
                              f"{'✅ Reviewed' if data.get('is_reviewed') else '🕒 Pending review'}"):

                col1, col2, col3 = st.columns(3)
                col1.metric("LSTM Class", data.get("lstm_prediction_class"))
                col2.metric("CNN Class", data.get("cnn_prediction_class"))
                col3.metric("ANN Class", data.get("ann_prediction_class"))

                if data.get("cnn_gradcam_path") and os.path.exists(data["cnn_gradcam_path"]):
                    st.image(data["cnn_gradcam_path"], caption="Grad-CAM overlay", width=350)

                st.markdown(f"**Summary:** {data.get('llm_summary', '')}")
                st.markdown(f"**Reasoning:** {data.get('llm_reasoning', '')}")
                st.markdown(f"**Mitigation:** {data.get('llm_mitigation', '')}")

                st.markdown("---")
                st.markdown("##### Human-in-the-Loop Review")
                with st.form(f"hitl_form_{data['id']}"):
                    hc1, hc2, hc3 = st.columns(3)
                    override_lstm = hc1.text_input("Override LSTM class", value="")
                    override_cnn = hc2.text_input("Override CNN class", value="")
                    override_ann = hc3.text_input("Override ANN class", value="")
                    reviewed_by = st.text_input("Reviewed by", value="Analyst")
                    notes = st.text_area("Analyst notes")
                    hitl_submit = st.form_submit_button("Submit Review")

                if hitl_submit:
                    db = get_session()
                    try:
                        record = db.query(AssetAssessment).filter(AssetAssessment.id == data["id"]).first()
                        record.is_reviewed = True
                        record.reviewed_by = reviewed_by
                        record.reviewed_at = datetime.utcnow()
                        if override_lstm.strip() != "":
                            record.override_lstm_class = int(override_lstm)
                        if override_cnn.strip() != "":
                            record.override_cnn_class = int(override_cnn)
                        if override_ann.strip() != "":
                            record.override_ann_class = int(override_ann)
                        if notes.strip() != "":
                            record.analyst_notes = notes
                        db.commit()
                        st.success("Review submitted.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Failed to submit review: {e}")
                    finally:
                        db.close()

                st.markdown("---")
                if st.button("Generate & Download PDF Report", key=f"pdf_{data['id']}"):
                    pdf_path = f"data/uploads/report_{data['id']}.pdf"
                    try:
                        generate_pdf_report(data, pdf_path)
                        with open(pdf_path, "rb") as f:
                            st.download_button(
                                label="Download PDF",
                                data=f.read(),
                                file_name=f"OmniRisk_Report_{data['asset_name'].replace(' ', '_')}_{data['id']}.pdf",
                                mime="application/pdf",
                                key=f"dl_{data['id']}",
                            )
                    except Exception as e:
                        st.error(f"PDF compilation failed: {e}")