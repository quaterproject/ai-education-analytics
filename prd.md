# MASTER PROJECT BUILD PROMPT

You are a **Senior AI Engineer, Machine Learning Engineer, Full-Stack Developer, Data Scientist, and Software Architect**.

Your task is to design and implement a complete, production-style AI web application called:

# EduPilot AI — Intelligent Student Success Co-Pilot

Build a fully functional **AI Co-Pilot for Education Analytics** that predicts student academic risk, analyzes multimodal student data, explains predictions using Explainable AI, and allows educators to approve, reject, or modify AI-generated intervention recommendations.

The project must satisfy all mandatory project requirements.

---

# 1. PROJECT OBJECTIVE

Build an AI-powered education analytics platform that helps teachers, academic advisors, schools, colleges, and universities identify students who may be academically at risk.

The application must process multiple data modalities:

1. Tabular student performance data.
2. PDF academic reports.
3. Images or scanned academic documents.
4. Text-based teacher or advisor notes.

The primary predictive engine must be a **deep learning Artificial Neural Network (ANN)**.

Large Language Models must NOT be used as the primary prediction model.

LLMs should only be used for:

- Reasoning.
- Recommendation generation.
- Student intervention planning.
- Prediction explanation.
- Summarization.
- Report generation.

The system must include:

- Multimodal data processing.
- ANN deep learning prediction.
- Explainable AI.
- Human-in-the-Loop workflow.
- AI-generated recommendations.
- Downloadable PDF and DOCX reports.
- Business-focused analytics.
- Production-style web interface.

---

# 2. CORE BUSINESS PROBLEM

Educational institutions often identify struggling students too late.

Student information is distributed across:

- Attendance records.
- Exam scores.
- Assignment performance.
- Demographic information.
- Teacher notes.
- Academic PDF reports.
- Scanned documents.

EduPilot AI should combine these sources and create a unified student risk assessment.

The system should answer:

- Is this student academically at risk?
- What is the predicted risk level?
- What factors contributed to the prediction?
- What intervention should an educator consider?
- How confident is the model?
- Does the educator approve the AI recommendation?

---

# 3. REQUIRED TECHNOLOGY STACK

## Backend

Use:

- Python 3.12+
- FastAPI
- Uvicorn
- Pydantic
- SQLAlchemy
- Alembic
- SQLite for development
- PostgreSQL-ready database configuration

## Python Package Management

MANDATORY:

Use `uv`.

DO NOT use:

- pip requirements.txt
- Poetry
- Pipenv

The project must contain:

```text
pyproject.toml
uv.lock
```

Use `pyproject.toml` for all dependencies.

The application should run using:

```bash
uv sync
uv run uvicorn app.main:app --reload
```

## Machine Learning

Use:

- PyTorch
- scikit-learn
- pandas
- numpy
- joblib

Primary predictive model:

```text
Artificial Neural Network (ANN)
```

The ANN must predict student academic risk.

Suggested output classes:

```text
LOW_RISK
MEDIUM_RISK
HIGH_RISK
```

The ANN must be the primary predictive engine.

## Explainable AI

Use:

- SHAP

Provide:

- SHAP feature importance.
- Global feature importance.
- Individual student feature contributions.
- Prediction confidence score.
- Positive risk factors.
- Protective factors.

## AI / LLM Integration

Use:

- LangChain
- OpenAI Chat Completions API
- Cohere model/API for OCR-style multimodal document and image text extraction

Use LangChain to orchestrate the AI workflows.

OpenAI Chat Completions must be used for:

- Student risk explanation.
- Intervention recommendation generation.
- Academic report summarization.
- Teacher-friendly explanations.
- Final report narrative generation.

Cohere must be used for:

- Extracting structured information from uploaded document images where supported.
- Processing OCR-style extracted content.
- Understanding scanned academic documents.
- Converting document content into structured academic information.

Create clean provider abstractions.

Do not tightly couple the application to one model name.

Model names must be configurable using environment variables.

Example:

```env
OPENAI_API_KEY=
OPENAI_MODEL=

COHERE_API_KEY=
COHERE_MODEL=
```

Create separate AI provider services.

Example:

```text
OpenAIService
CohereDocumentService
```

All LLM prompts must be stored separately from business logic.

---

# 4. FRONTEND

Use:

- React
- TypeScript
- Vite
- Tailwind CSS
- shadcn/ui
- React Router
- TanStack Query
- Axios
- Recharts
- Lucide React

Build a modern SaaS-style AI dashboard.

The interface should look like a commercial AI analytics product.

Design characteristics:

- Clean.
- Professional.
- Modern.
- Minimal.
- Responsive.
- Education-focused.
- Enterprise dashboard style.

Do not create a basic university assignment interface.

Create a polished AI SaaS product.

---

# 5. COMPLETE PROJECT STRUCTURE

Create the following monorepo structure:

```text
edupilot-ai/
│
├── README.md
├── .gitignore
├── .env.example
├── docker-compose.yml
│
├── backend/
│   ├── pyproject.toml
│   ├── uv.lock
│   ├── alembic.ini
│   │
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   │
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── config.py
│   │   │   ├── database.py
│   │   │   ├── logging.py
│   │   │   ├── exceptions.py
│   │   │   └── constants.py
│   │   │
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── dependencies.py
│   │   │   │
│   │   │   └── v1/
│   │   │       ├── __init__.py
│   │   │       ├── router.py
│   │   │       └── endpoints/
│   │   │           ├── __init__.py
│   │   │           ├── health.py
│   │   │           ├── students.py
│   │   │           ├── predictions.py
│   │   │           ├── documents.py
│   │   │           ├── recommendations.py
│   │   │           ├── reviews.py
│   │   │           ├── analytics.py
│   │   │           └── reports.py
│   │   │
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── student.py
│   │   │   ├── academic_record.py
│   │   │   ├── document.py
│   │   │   ├── prediction.py
│   │   │   ├── recommendation.py
│   │   │   └── human_review.py
│   │   │
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── student.py
│   │   │   ├── academic_record.py
│   │   │   ├── document.py
│   │   │   ├── prediction.py
│   │   │   ├── recommendation.py
│   │   │   ├── review.py
│   │   │   ├── analytics.py
│   │   │   └── report.py
│   │   │
│   │   ├── repositories/
│   │   │   ├── __init__.py
│   │   │   ├── student_repository.py
│   │   │   ├── document_repository.py
│   │   │   ├── prediction_repository.py
│   │   │   └── review_repository.py
│   │   │
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── student_service.py
│   │   │   ├── prediction_service.py
│   │   │   ├── multimodal_service.py
│   │   │   ├── recommendation_service.py
│   │   │   ├── explainability_service.py
│   │   │   ├── human_review_service.py
│   │   │   ├── analytics_service.py
│   │   │   └── report_service.py
│   │   │
│   │   ├── ai/
│   │   │   ├── __init__.py
│   │   │   │
│   │   │   ├── providers/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── openai_service.py
│   │   │   │   └── cohere_document_service.py
│   │   │   │
│   │   │   ├── chains/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── explanation_chain.py
│   │   │   │   ├── recommendation_chain.py
│   │   │   │   ├── document_analysis_chain.py
│   │   │   │   └── report_chain.py
│   │   │   │
│   │   │   ├── prompts/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── explanation_prompts.py
│   │   │   │   ├── recommendation_prompts.py
│   │   │   │   ├── document_prompts.py
│   │   │   │   └── report_prompts.py
│   │   │   │
│   │   │   └── parsers/
│   │   │       ├── __init__.py
│   │   │       ├── academic_parser.py
│   │   │       └── recommendation_parser.py
│   │   │
│   │   ├── ml/
│   │   │   ├── __init__.py
│   │   │   │
│   │   │   ├── models/
│   │   │   │   ├── __init__.py
│   │   │   │   └── student_risk_ann.py
│   │   │   │
│   │   │   ├── training/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── train.py
│   │   │   │   ├── evaluate.py
│   │   │   │   └── dataset.py
│   │   │   │
│   │   │   ├── preprocessing/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── feature_engineering.py
│   │   │   │   └── preprocessor.py
│   │   │   │
│   │   │   ├── inference/
│   │   │   │   ├── __init__.py
│   │   │   │   └── predictor.py
│   │   │   │
│   │   │   └── explainability/
│   │   │       ├── __init__.py
│   │   │       └── shap_explainer.py
│   │   │
│   │   ├── multimodal/
│   │   │   ├── __init__.py
│   │   │   ├── pdf_processor.py
│   │   │   ├── image_processor.py
│   │   │   ├── text_processor.py
│   │   │   ├── tabular_processor.py
│   │   │   └── feature_fusion.py
│   │   │
│   │   ├── reports/
│   │   │   ├── __init__.py
│   │   │   ├── pdf_generator.py
│   │   │   ├── docx_generator.py
│   │   │   └── templates.py
│   │   │
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── file_utils.py
│   │       ├── validation.py
│   │       └── helpers.py
│   │
│   ├── alembic/
│   │   ├── env.py
│   │   └── versions/
│   │
│   ├── data/
│   │   ├── raw/
│   │   ├── processed/
│   │   └── sample/
│   │
│   ├── artifacts/
│   │   ├── models/
│   │   ├── preprocessors/
│   │   └── explainers/
│   │
│   ├── uploads/
│   │
│   ├── generated_reports/
│   │
│   ├── scripts/
│   │   ├── download_dataset.py
│   │   ├── prepare_dataset.py
│   │   ├── train_model.py
│   │   └── seed_database.py
│   │
│   └── tests/
│       ├── __init__.py
│       ├── test_students.py
│       ├── test_predictions.py
│       ├── test_documents.py
│       ├── test_reviews.py
│       └── test_reports.py
│
└── frontend/
    ├── package.json
    ├── vite.config.ts
    ├── tsconfig.json
    ├── components.json
    ├── tailwind.config.ts
    ├── .env.example
    │
    └── src/
        ├── main.tsx
        ├── App.tsx
        │
        ├── api/
        │   ├── client.ts
        │   ├── students.ts
        │   ├── predictions.ts
        │   ├── documents.ts
        │   ├── reviews.ts
        │   ├── analytics.ts
        │   └── reports.ts
        │
        ├── components/
        │   ├── ui/
        │   ├── layout/
        │   │   ├── AppSidebar.tsx
        │   │   ├── Header.tsx
        │   │   └── PageContainer.tsx
        │   │
        │   ├── dashboard/
        │   │   ├── StatsCard.tsx
        │   │   ├── RiskDistributionChart.tsx
        │   │   ├── RiskTrendChart.tsx
        │   │   └── RecentPredictions.tsx
        │   │
        │   ├── students/
        │   │   ├── StudentTable.tsx
        │   │   ├── StudentForm.tsx
        │   │   └── StudentProfileCard.tsx
        │   │
        │   ├── prediction/
        │   │   ├── RiskScoreCard.tsx
        │   │   ├── ConfidenceGauge.tsx
        │   │   ├── FeatureImportanceChart.tsx
        │   │   ├── RiskFactors.tsx
        │   │   └── ProtectiveFactors.tsx
        │   │
        │   ├── documents/
        │   │   ├── DocumentUploader.tsx
        │   │   ├── ProcessingStatus.tsx
        │   │   └── ExtractedDataPreview.tsx
        │   │
        │   ├── recommendations/
        │   │   ├── RecommendationCard.tsx
        │   │   └── InterventionPlan.tsx
        │   │
        │   └── reviews/
        │       └── HumanReviewPanel.tsx
        │
        ├── pages/
        │   ├── DashboardPage.tsx
        │   ├── StudentsPage.tsx
        │   ├── StudentDetailPage.tsx
        │   ├── NewAssessmentPage.tsx
        │   ├── PredictionPage.tsx
        │   ├── ReviewQueuePage.tsx
        │   ├── AnalyticsPage.tsx
        │   └── ReportsPage.tsx
        │
        ├── hooks/
        │   ├── useStudents.ts
        │   ├── usePrediction.ts
        │   ├── useDocuments.ts
        │   └── useReviews.ts
        │
        ├── types/
        │   ├── student.ts
        │   ├── prediction.ts
        │   ├── document.ts
        │   └── review.ts
        │
        ├── lib/
        │   └── utils.ts
        │
        └── styles/
            └── globals.css
```

---

# 6. DATASET

Use the UCI Student Performance dataset as the initial training dataset.

Support the student mathematics and Portuguese datasets.

The dataset contains features such as:

- Age.
- Gender.
- School.
- Family size.
- Parent education.
- Study time.
- Previous failures.
- School support.
- Family support.
- Paid classes.
- Extracurricular activities.
- Internet access.
- Romantic relationship.
- Family relationship quality.
- Free time.
- Going out frequency.
- Alcohol consumption.
- Health.
- Absences.
- Grade 1.
- Grade 2.
- Final grade.

Create a dataset preparation script.

The script must:

1. Load the raw dataset.
2. Handle missing values.
3. Encode categorical features.
4. Scale numerical features.
5. Engineer relevant features.
6. Create risk labels.
7. Split training, validation, and testing data.
8. Save the fitted preprocessor.
9. Save processed datasets.

Suggested risk classification:

```text
Final Grade >= 14:
LOW_RISK

Final Grade >= 10 and < 14:
MEDIUM_RISK

Final Grade < 10:
HIGH_RISK
```

Avoid direct target leakage.

When predicting risk, do not use the final grade as an input feature if the risk label was generated from the final grade.

Carefully analyze G1 and G2 for potential leakage and document the decision.

Create two model configurations if useful:

```text
EARLY_WARNING
LATE_STAGE
```

EARLY_WARNING should avoid later academic grade features.

LATE_STAGE may use available intermediate academic performance.

Clearly explain this distinction.

---

# 7. ANN DEEP LEARNING MODEL

Create a PyTorch ANN.

Suggested architecture:

```text
Input Features
      ↓
Linear Layer
      ↓
Batch Normalization
      ↓
ReLU
      ↓
Dropout
      ↓
Linear Layer
      ↓
Batch Normalization
      ↓
ReLU
      ↓
Dropout
      ↓
Linear Layer
      ↓
Softmax Risk Classes
```

Example conceptual architecture:

```text
Input
↓
128 neurons
↓
64 neurons
↓
32 neurons
↓
3 output classes
```

Use:

- CrossEntropyLoss.
- AdamW optimizer.
- Learning rate scheduler.
- Early stopping.
- Dropout.
- Batch normalization.

Track:

- Training loss.
- Validation loss.
- Accuracy.
- Precision.
- Recall.
- F1 score.

Generate:

- Classification report.
- Confusion matrix.
- Training history.

Save:

```text
student_risk_ann.pt
preprocessor.joblib
label_encoder.joblib
model_metadata.json
```

The application must load the trained model during FastAPI startup.

Do not retrain the model for every API request.

---

# 8. MULTIMODAL PROCESSING

The system must process at least four modalities.

## Modality 1: Tabular Data

Process:

- Attendance.
- Grades.
- Study time.
- Failures.
- Student behavior variables.
- Academic features.

Use the ANN for prediction.

## Modality 2: PDF Documents

Allow users to upload:

```text
.pdf
```

Examples:

- Academic report.
- Grade report.
- Attendance report.
- Student evaluation.

Extract text from digitally generated PDFs.

If normal text extraction produces insufficient text, process the document using the document/image analysis workflow.

Extract structured fields such as:

```json
{
  "student_name": "",
  "student_id": "",
  "subjects": [],
  "grades": [],
  "attendance": null,
  "teacher_comments": [],
  "academic_concerns": []
}
```

## Modality 3: Images

Allow:

```text
.png
.jpg
.jpeg
.webp
```

Use the Cohere document/vision processing service where supported by the configured model.

The service should analyze academic document images and return structured academic data.

Do not hardcode an unsupported API contract.

Create a provider adapter that validates model capabilities.

If the configured Cohere model does not support direct image input, use a clearly isolated OCR fallback provider and pass the extracted text to Cohere for structured understanding.

The architecture must remain clean and provider-independent.

Never silently fake OCR results.

Return a clear processing error if no supported OCR or vision capability is configured.

## Modality 4: Text

Allow educators to enter teacher notes.

Example:

```text
The student has missed several classes recently.
Assignment completion has declined.
The student appears disengaged during mathematics lessons.
```

Use OpenAI through LangChain to convert teacher notes into structured contextual signals.

Example:

```json
{
  "attendance_concern": true,
  "engagement_concern": true,
  "assignment_concern": true,
  "behavioral_concern": false,
  "summary": ""
}
```

---

# 9. MULTIMODAL FEATURE FUSION

Create:

```text
feature_fusion.py
```

Combine information from:

- ANN tabular features.
- PDF extracted academic information.
- Image document information.
- Teacher notes.

Important:

The ANN prediction must remain the primary predictive result.

LLM output must not directly replace the ANN risk classification.

Create an architecture similar to:

```text
Student Tabular Data
        ↓
ANN Prediction
        ↓
Base Risk Prediction

PDF ──────────────┐
Image Document ───┼── Context Extraction
Teacher Notes ────┘
                         ↓
               Contextual Evidence
                         ↓
ANN Prediction + SHAP + Context
                         ↓
                 LLM Reasoning
                         ↓
             Intervention Recommendation
```

The LLM receives:

- ANN prediction.
- ANN confidence.
- SHAP factors.
- Extracted document evidence.
- Teacher note context.

The LLM generates recommendations.

It MUST NOT override the ANN model's prediction.

---

# 10. EXPLAINABLE AI

Implement SHAP explainability.

For each prediction return:

```json
{
  "risk_level": "HIGH_RISK",
  "confidence": 0.91,
  "class_probabilities": {
    "LOW_RISK": 0.03,
    "MEDIUM_RISK": 0.06,
    "HIGH_RISK": 0.91
  },
  "top_risk_factors": [],
  "protective_factors": [],
  "feature_contributions": []
}
```

Example risk factors:

```text
High previous failure count
Low study time
High absence rate
Declining intermediate grades
Low academic support
```

Example protective factors:

```text
Strong family support
Regular internet access
Good historical performance
```

Display SHAP values in the frontend.

Create:

- Horizontal feature importance chart.
- Risk factor cards.
- Protective factor cards.

The UI must clearly state:

```text
AI predictions are decision-support recommendations and require educator review.
```

---

# 11. LANGCHAIN ARCHITECTURE

Use LangChain.

Create separate chains.

## Explanation Chain

Input:

```text
ANN prediction
Confidence
SHAP factors
Student academic context
```

Output:

```json
{
  "summary": "",
  "risk_explanation": "",
  "key_concerns": [],
  "protective_observations": []
}
```

The explanation must use teacher-friendly language.

Do not claim certainty.

Avoid medical or psychological diagnoses.

## Recommendation Chain

Generate an intervention recommendation.

Output:

```json
{
  "title": "",
  "priority": "HIGH",
  "summary": "",
  "recommended_actions": [],
  "monitoring_plan": [],
  "success_indicators": [],
  "review_period_days": 14
}
```

Possible interventions:

- Academic counseling.
- Attendance monitoring.
- Tutoring.
- Parent or guardian communication.
- Study plan.
- Assignment monitoring.
- Peer support.
- Academic advisor meeting.

The model must not make medical diagnoses.

## Document Analysis Chain

Analyze extracted academic document text.

Return strict structured data.

Use Pydantic models and LangChain structured output.

## Report Chain

Generate a professional academic risk assessment narrative.

The report must clearly separate:

- Predictive model output.
- Explainability results.
- Document evidence.
- Teacher notes.
- AI recommendation.
- Human educator decision.

---

# 12. OPENAI SERVICE

Create:

```text
app/ai/providers/openai_service.py
```

Use LangChain's OpenAI chat integration.

Use the OpenAI Chat Completions-compatible chat model integration.

The API key and model must come from environment variables.

Do not hardcode API keys.

Implement:

- Async calls where supported.
- Timeout handling.
- Retry handling.
- Structured logging.
- Error handling.

Use temperature settings appropriate for the task.

Suggested behavior:

```text
Document extraction: 0
Risk explanation: 0.2
Recommendation: 0.3
Report narrative: 0.2
```

Do not expose internal chain-of-thought.

Request concise structured explanations and evidence-based summaries.

---

# 13. COHERE DOCUMENT SERVICE

Create:

```text
app/ai/providers/cohere_document_service.py
```

The service must isolate all Cohere integration logic.

Responsibilities:

- Accept document image processing requests.
- Validate configured model capabilities.
- Process supported document content.
- Structure extracted academic information.
- Return normalized document text or structured data.
- Handle API errors.
- Handle unsupported image models.
- Handle invalid documents.

Create an interface similar to:

```python
class CohereDocumentService:
    async def analyze_document_image(self, file_path: str):
        ...

    async def structure_document_text(self, text: str):
        ...
```

Do not pretend Cohere provides a dedicated OCR endpoint if the selected SDK/model does not support one.

Use current SDK capabilities.

Keep OCR extraction and semantic document understanding conceptually separate.

The final architecture should allow another OCR provider to be added without changing the business services.

---

# 14. HUMAN-IN-THE-LOOP WORKFLOW

This is a mandatory requirement.

Every AI intervention recommendation must have a review status.

Statuses:

```text
PENDING_REVIEW
APPROVED
REJECTED
MODIFIED
```

Create a review queue.

The educator must be able to:

```text
Approve Recommendation
Reject Recommendation
Modify Recommendation
```

## Approve

Store:

```text
status = APPROVED
reviewed_by
reviewed_at
educator_comment
```

## Reject

Require a rejection reason.

Store:

```text
status = REJECTED
rejection_reason
reviewed_by
reviewed_at
```

## Modify

Allow the educator to edit:

- Recommendation title.
- Summary.
- Recommended actions.
- Monitoring plan.
- Review period.

Store:

```text
original_ai_recommendation
modified_recommendation
status = MODIFIED
```

Never overwrite the original AI output.

Maintain a complete audit trail.

Display:

```text
AI Generated Recommendation
```

and:

```text
Final Educator Approved Plan
```

as separate sections.

---

# 15. DATABASE MODELS

Create database models for:

## Student

Fields:

```text
id
student_code
first_name
last_name
age
gender
school
created_at
updated_at
```

## AcademicRecord

```text
id
student_id
study_time
failures
absences
family_support
school_support
internet_access
health
g1
g2
created_at
```

## Document

```text
id
student_id
filename
file_type
file_path
processing_status
extracted_text
structured_data
created_at
```

## Prediction

```text
id
student_id
risk_level
confidence
class_probabilities
model_version
feature_values
shap_values
risk_factors
protective_factors
created_at
```

## Recommendation

```text
id
prediction_id
title
priority
summary
recommended_actions
monitoring_plan
success_indicators
review_period_days
llm_model
created_at
```

## HumanReview

```text
id
recommendation_id
status
reviewed_by
educator_comment
rejection_reason
original_recommendation
modified_recommendation
reviewed_at
created_at
```

Use proper relationships.

Use UUIDs where appropriate.

---

# 16. API ENDPOINTS

Use API prefix:

```text
/api/v1
```

Implement:

## Health

```text
GET /api/v1/health
```

## Students

```text
GET    /api/v1/students
POST   /api/v1/students
GET    /api/v1/students/{student_id}
PUT    /api/v1/students/{student_id}
DELETE /api/v1/students/{student_id}
```

## Documents

```text
POST /api/v1/students/{student_id}/documents
GET  /api/v1/students/{student_id}/documents
GET  /api/v1/documents/{document_id}
```

## Predictions

```text
POST /api/v1/students/{student_id}/predict
GET  /api/v1/students/{student_id}/predictions
GET  /api/v1/predictions/{prediction_id}
```

## Recommendations

```text
POST /api/v1/predictions/{prediction_id}/recommendation
GET  /api/v1/recommendations/{recommendation_id}
```

## Human Reviews

```text
GET  /api/v1/reviews/pending
POST /api/v1/recommendations/{recommendation_id}/approve
POST /api/v1/recommendations/{recommendation_id}/reject
POST /api/v1/recommendations/{recommendation_id}/modify
```

## Analytics

```text
GET /api/v1/analytics/overview
GET /api/v1/analytics/risk-distribution
GET /api/v1/analytics/risk-trends
GET /api/v1/analytics/intervention-status
```

## Reports

```text
POST /api/v1/students/{student_id}/reports/pdf
POST /api/v1/students/{student_id}/reports/docx
GET  /api/v1/reports/{report_id}/download
```

Use proper HTTP status codes.

Create OpenAPI documentation.

---

# 17. FRONTEND PAGES

## Dashboard

Display:

- Total students.
- High-risk students.
- Medium-risk students.
- Low-risk students.
- Pending human reviews.
- Risk distribution chart.
- Risk trend chart.
- Recent predictions.

## Students Page

Display a searchable student table.

Columns:

```text
Student
School
Latest Risk
Confidence
Last Assessment
Review Status
Actions
```

## Student Detail Page

Display:

- Student profile.
- Academic information.
- Uploaded documents.
- Teacher notes.
- Prediction history.
- Intervention history.

Include:

```text
Run New Assessment
```

button.

## New Assessment Page

Create a multi-step workflow.

### Step 1

Student academic data.

### Step 2

Upload PDF or academic document image.

### Step 3

Enter teacher notes.

### Step 4

Review multimodal information.

### Step 5

Run ANN risk prediction.

Show processing states.

Example:

```text
Processing academic data...
Analyzing uploaded document...
Extracting contextual evidence...
Running ANN risk model...
Calculating SHAP explanations...
Generating educator recommendation...
```

## Prediction Page

Display a large risk card.

Example:

```text
HIGH RISK

91% Model Confidence
```

Display class probabilities.

Display:

- AI explanation.
- Top risk factors.
- Protective factors.
- SHAP feature contribution chart.
- Document evidence.
- Teacher note context.

Clearly label:

```text
ANN Predictive Model Result
```

and:

```text
LLM Generated Explanation
```

Do not mix the two.

## Review Queue

Display all recommendations with:

```text
PENDING_REVIEW
```

Create the Human Review Panel.

Buttons:

```text
Approve
Modify
Reject
```

Use confirmation dialogs.

## Analytics Page

Display:

- Risk distribution.
- Risk trends.
- Most common risk factors.
- Intervention approval rate.
- Recommendation modification rate.
- High-risk student trend.

## Reports Page

Allow report generation.

Buttons:

```text
Generate PDF
Generate DOCX
Download Report
```

---

# 18. REPORT GENERATION

Generate both:

```text
PDF
DOCX
```

The report should contain:

# EduPilot AI Student Risk Assessment

## Student Information

Student details.

## Academic Data Summary

Academic performance information.

## Predictive Model Assessment

Include:

```text
Risk Level
Confidence
Class Probabilities
Model Version
```

Clearly state:

```text
Prediction generated by the EduPilot ANN risk classification model.
```

## Explainable AI Analysis

Include:

- Top risk factors.
- Protective factors.
- Feature contributions.

## Multimodal Evidence

Include:

- PDF evidence.
- Image document evidence.
- Teacher notes.

## AI Co-Pilot Recommendation

Include the LLM-generated intervention plan.

## Human Educator Review

Include:

```text
Review Status
Educator Decision
Educator Comments
Modification Details
Review Date
```

## Disclaimer

Include:

```text
EduPilot AI is a decision-support system. Predictions and AI-generated recommendations are intended to assist qualified educators and academic advisors. Final academic intervention decisions remain the responsibility of the educational institution and authorized personnel.
```

Use ReportLab for PDF generation.

Use python-docx for DOCX generation.

---

# 19. BUSINESS MODEL

Create a business and commercialization section in the README.

Business model:

```text
B2B SaaS
```

Target customers:

- Schools.
- Colleges.
- Universities.
- Online learning platforms.
- Academic counseling organizations.

Pricing concept:

```text
Starter:
Small schools

Professional:
Medium institutions

Enterprise:
Universities and education networks
```

Possible pricing model:

```text
Per active student per month
```

or:

```text
Annual institutional license
```

Commercial value:

- Earlier identification of at-risk students.
- Reduced student dropout.
- Better academic interventions.
- Centralized academic evidence.
- Explainable predictions.
- Human-controlled AI recommendations.
- Institutional reporting.

Include commercialization strategy:

1. Pilot with schools.
2. Validate prediction accuracy.
3. Measure intervention outcomes.
4. Integrate with Student Information Systems.
5. Add LMS integrations.
6. Expand into enterprise education analytics.

---

# 20. SECURITY AND PRIVACY

Student information is sensitive.

Implement:

- Environment variable secrets.
- File type validation.
- File size validation.
- Sanitized filenames.
- UUID-based stored filenames.
- API validation.
- CORS configuration.
- Structured error responses.

Do not log:

- API keys.
- Full student documents.
- Sensitive document text.

Add a privacy notice to the README.

Clearly state that a production system must implement:

- Authentication.
- Role-Based Access Control.
- Data encryption.
- Institutional data retention policies.
- FERPA/GDPR assessment where applicable.

Do not claim legal compliance unless the required controls have actually been implemented and audited.

---

# 21. PYPROJECT.TOML

Create a valid `pyproject.toml`.

Use a modern Python project configuration compatible with `uv`.

Include dependencies required by the implemented application.

Expected dependency categories include:

```text
fastapi
uvicorn
pydantic
pydantic-settings
sqlalchemy
alembic
python-multipart
aiosqlite
psycopg
pandas
numpy
scikit-learn
torch
shap
joblib
langchain
langchain-openai
cohere
pypdf
pillow
reportlab
python-docx
httpx
tenacity
```

Add development dependencies:

```text
pytest
pytest-asyncio
ruff
mypy
```

Do not add unused libraries.

Use the actual package names required by the final implementation.

---

# 22. ENVIRONMENT CONFIGURATION

Create:

```text
.env.example
```

Example:

```env
APP_NAME=EduPilot AI
APP_ENV=development
DEBUG=true

DATABASE_URL=sqlite+aiosqlite:///./edupilot.db

OPENAI_API_KEY=
OPENAI_MODEL=

COHERE_API_KEY=
COHERE_MODEL=

MODEL_PATH=./artifacts/models/student_risk_ann.pt
PREPROCESSOR_PATH=./artifacts/preprocessors/preprocessor.joblib

UPLOAD_DIR=./uploads
REPORT_DIR=./generated_reports

MAX_UPLOAD_SIZE_MB=10

FRONTEND_URL=http://localhost:5173
```

Never include real secrets.

---

# 23. ERROR HANDLING

Create consistent API errors.

Example:

```json
{
  "error": {
    "code": "DOCUMENT_PROCESSING_FAILED",
    "message": "The uploaded academic document could not be processed.",
    "details": null
  }
}
```

Handle:

- Invalid student.
- Missing model.
- Model loading failure.
- Invalid academic data.
- Unsupported file.
- Large file.
- PDF extraction failure.
- OCR/vision failure.
- OpenAI failure.
- Cohere failure.
- Recommendation failure.
- Report generation failure.

Do not expose stack traces to frontend users.

---

# 24. TESTING

Create backend tests.

Test:

- Student creation.
- Student retrieval.
- Prediction validation.
- ANN inference service.
- Document upload validation.
- PDF processing.
- Human approval.
- Human rejection.
- Recommendation modification.
- Report generation.

Mock external AI APIs.

Do not call paid OpenAI or Cohere APIs during tests.

Use dependency injection or provider mocks.

---

# 25. README

Create a professional README.

Include:

1. Project overview.
2. Business problem.
3. Solution.
4. Features.
5. Architecture.
6. Multimodal workflow.
7. ANN predictive model.
8. Explainable AI.
9. Human-in-the-Loop workflow.
10. Technology stack.
11. Folder structure.
12. Installation.
13. Environment variables.
14. Dataset preparation.
15. Model training.
16. Backend startup.
17. Frontend startup.
18. API documentation.
19. Report generation.
20. Business model.
21. Commercialization strategy.
22. Privacy considerations.
23. Limitations.
24. Future improvements.

Add Mermaid architecture diagrams.

Create a diagram for:

```text
Frontend
↓
FastAPI
↓
Multimodal Processing
↓
ANN Risk Model
↓
SHAP
↓
LangChain
↓
OpenAI / Cohere Document Processing
↓
AI Recommendation
↓
Human Review
↓
Approved Intervention
↓
PDF / DOCX Report
```

---

# 26. CODE QUALITY REQUIREMENTS

Follow these rules:

- Use type hints.
- Use async APIs where appropriate.
- Use Pydantic schemas.
- Separate API routes from services.
- Separate services from repositories.
- Separate ML inference from AI reasoning.
- Do not place all logic in `main.py`.
- Do not create giant files.
- Avoid duplicated code.
- Use dependency injection.
- Use descriptive variable names.
- Add docstrings to important services.
- Add structured logging.
- Follow SOLID principles where practical.

Important architectural rule:

```text
ANN = Prediction

SHAP = Prediction Explanation

OpenAI = Reasoning and Recommendation

Cohere Document Service = Document/Image Understanding Pipeline

Human Educator = Final Decision
```

Never violate this separation.

---

# 27. UI QUALITY REQUIREMENTS

The frontend must feel like a real commercial product.

Create:

- Professional sidebar.
- Dashboard header.
- Responsive layouts.
- Loading skeletons.
- Empty states.
- Error states.
- Toast notifications.
- Confirmation dialogs.
- Status badges.
- Risk badges.
- Tooltips.

Risk levels:

```text
LOW RISK
MEDIUM RISK
HIGH RISK
```

Review states:

```text
PENDING
APPROVED
REJECTED
MODIFIED
```

Use icons from Lucide React.

Do not use emojis as primary interface icons.

Do not create excessive gradients.

Do not create a generic AI chatbot interface.

This is an AI analytics and decision-support dashboard.

---

# 28. IMPLEMENTATION ORDER

Build the project in the following order.

## Phase 1

Create the folder structure.

Create backend `pyproject.toml`.

Configure `uv`.

Create FastAPI application.

Configure settings.

Configure database.

Create database models.

Create Alembic configuration.

## Phase 2

Create dataset scripts.

Create preprocessing pipeline.

Create ANN model.

Create training pipeline.

Create evaluation pipeline.

Save model artifacts.

## Phase 3

Create ANN inference service.

Create SHAP explainer.

Create prediction APIs.

## Phase 4

Create PDF processor.

Create image document processor.

Create text processor.

Create tabular processor.

Create multimodal feature fusion.

## Phase 5

Create LangChain architecture.

Create OpenAI provider.

Create Cohere document provider.

Create explanation chain.

Create recommendation chain.

Create document analysis chain.

Create report chain.

## Phase 6

Create Human-in-the-Loop workflow.

Create approval.

Create rejection.

Create modification.

Create audit trail.

## Phase 7

Create PDF reports.

Create DOCX reports.

Create download APIs.

## Phase 8

Create React frontend.

Create dashboard.

Create student pages.

Create assessment workflow.

Create prediction visualization.

Create SHAP visualization.

Create review queue.

Create reports page.

## Phase 9

Create tests.

Create seed data.

Create README.

Verify all application flows.

---

# 29. FINAL ACCEPTANCE CRITERIA

The final application is complete only if:

- It processes tabular student data.
- It processes PDF documents.
- It processes academic document images.
- It processes teacher text notes.
- A PyTorch ANN performs risk prediction.
- The LLM is not the primary predictor.
- SHAP explains ANN predictions.
- Prediction confidence is displayed.
- Risk factors are displayed.
- Protective factors are displayed.
- LangChain orchestrates LLM workflows.
- OpenAI Chat Completions integration is implemented.
- Cohere document processing integration is isolated in a provider service.
- Human users can approve recommendations.
- Human users can reject recommendations.
- Human users can modify recommendations.
- Original AI recommendations are preserved.
- PDF reports can be generated.
- DOCX reports can be generated.
- Reports can be downloaded.
- The frontend is responsive.
- The application has a professional SaaS interface.
- `uv` is used for Python package management.
- `pyproject.toml` exists.
- No `requirements.txt` is used.
- API keys are stored in environment variables.
- External APIs are mocked during tests.
- The README explains the business model.
- The README explains commercialization strategy.
- The application runs locally.

---

# 30. EXECUTION INSTRUCTION

Now implement the complete project.

Do not only provide explanations or pseudocode.

Create the actual files and write complete working code.

Start by creating the full project structure.

Then implement each phase in order.

For every file:

- Write complete code.
- Ensure imports are correct.
- Ensure file paths are correct.
- Ensure frontend API paths match backend routes.
- Ensure Pydantic schemas match API responses.
- Ensure SQLAlchemy models and relationships work.
- Ensure the ANN input dimension matches the saved preprocessor output.
- Ensure SHAP works with the implemented PyTorch ANN.
- Ensure LangChain structured outputs match Pydantic schemas.
- Ensure OpenAI and Cohere integrations are configurable.
- Ensure external API failures are handled.
- Ensure the application can run without hidden or missing source files.

Do not leave critical functionality as:

```text
TODO
pass
implement later
mock this in production
```

Mocks are allowed only inside automated tests.

If an external model capability differs from an assumption, inspect the installed SDK/API capability and implement a valid adapter rather than inventing unsupported methods.

Before declaring completion:

1. Verify backend imports.
2. Verify `uv sync`.
3. Verify database initialization and migrations.
4. Verify model training command.
5. Verify model inference.
6. Verify FastAPI startup.
7. Verify frontend build.
8. Verify API integration.
9. Verify report generation.
10. Verify Human-in-the-Loop workflow.

Build EduPilot AI as a complete, modular, professional AI education analytics product.
