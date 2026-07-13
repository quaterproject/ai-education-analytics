import os
import json
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Float, Text, Boolean, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

DATABASE_URI = os.getenv("DATABASE_URI")
if not DATABASE_URI:
    raise ValueError("DATABASE_URI environment variable is not set")

engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class AssetAssessment(Base):
    __tablename__ = "asset_assessments"

    id = Column(Integer, primary_key=True, index=True)
    asset_name = Column(String(100), nullable=False)
    location = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Input file paths
    sensor_csv_path = Column(String(255), nullable=True)
    image_path = Column(String(255), nullable=True)
    audio_path = Column(String(255), nullable=True)

    # Deep learning predictions & explainability (LSTM)
    lstm_prediction_class = Column(Integer, nullable=True)  # 0=Low, 1=Medium, 2=High
    lstm_confidence_scores = Column(Text, nullable=True)   # JSON string
    lstm_feature_importance = Column(Text, nullable=True)  # JSON string

    # Deep learning predictions & explainability (CNN)
    cnn_prediction_class = Column(Integer, nullable=True)  # 0=Healthy, 1=Damaged
    cnn_confidence_score = Column(Float, nullable=True)
    cnn_gradcam_path = Column(String(255), nullable=True)

    # Deep learning predictions (ANN Audio)
    ann_prediction_class = Column(Integer, nullable=True)  # 0=Normal, 1=Anomalous
    ann_confidence_score = Column(Float, nullable=True)

    # LLM reasoning & report text
    llm_summary = Column(Text, nullable=True)
    llm_reasoning = Column(Text, nullable=True)
    llm_mitigation = Column(Text, nullable=True)

    # Human-In-The-Loop (HITL) overrides
    is_reviewed = Column(Boolean, default=False)
    override_lstm_class = Column(Integer, nullable=True)
    override_cnn_class = Column(Integer, nullable=True)
    override_ann_class = Column(Integer, nullable=True)
    analyst_notes = Column(Text, nullable=True)
    reviewed_by = Column(String(100), nullable=True)
    reviewed_at = Column(DateTime, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "asset_name": self.asset_name,
            "location": self.location,
            "description": self.description,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "sensor_csv_path": self.sensor_csv_path,
            "image_path": self.image_path,
            "audio_path": self.audio_path,
            "lstm_prediction_class": self.lstm_prediction_class,
            "lstm_confidence_scores": json.loads(self.lstm_confidence_scores) if self.lstm_confidence_scores else [],
            "lstm_feature_importance": json.loads(self.lstm_feature_importance) if self.lstm_feature_importance else {},
            "cnn_prediction_class": self.cnn_prediction_class,
            "cnn_confidence_score": self.cnn_confidence_score,
            "cnn_gradcam_path": self.cnn_gradcam_path,
            "ann_prediction_class": self.ann_prediction_class,
            "ann_confidence_score": self.ann_confidence_score,
            "llm_summary": self.llm_summary,
            "llm_reasoning": self.llm_reasoning,
            "llm_mitigation": self.llm_mitigation,
            "is_reviewed": self.is_reviewed,
            "override_lstm_class": self.override_lstm_class,
            "override_cnn_class": self.override_cnn_class,
            "override_ann_class": self.override_ann_class,
            "analyst_notes": self.analyst_notes,
            "reviewed_by": self.reviewed_by,
            "reviewed_at": self.reviewed_at.isoformat() if self.reviewed_at else None
        }

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
