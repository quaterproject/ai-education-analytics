import requests
import json
import os

BASE_URL = "http://localhost:8000"

print("--- Step 1: Testing Root Endpoint ---")
try:
    res = requests.get(BASE_URL + "/")
    print("Response:", res.status_code, res.json())
except Exception as e:
    print("Failed to reach backend root:", e)
    exit(1)

print("\n--- Step 2: Posting New Assessment (Multimodal Pipeline) ---")
# Upload sample files
csv_path = "data/samples/sample_sensor_data.csv"
img_path = "data/samples/sample_damaged.png"
audio_path = "data/samples/sample_audio_features.csv"

payload = {
    "asset_name": "Hydro-Pump Beta",
    "location": "Substation 3",
    "description": "Inspect vibration levels and structural surface stress."
}

files = {}
if os.path.exists(csv_path):
    files["sensor_csv"] = open(csv_path, "rb")
if os.path.exists(img_path):
    files["image_file"] = open(img_path, "rb")
if os.path.exists(audio_path):
    files["audio_file"] = open(audio_path, "rb")

try:
    res = requests.post(BASE_URL + "/api/assessments", data=payload, files=files)
    print("Status Code:", res.status_code)
    if res.status_code != 200:
        print("Error Details:", res.text)
        exit(1)
    
    assessment = res.json()
    print("Successfully Created Assessment!")
    print("Assessment ID:", assessment["id"])
    print("LSTM Pred Class:", assessment["lstm_prediction_class"])
    print("LSTM Feature Importance:", assessment["lstm_feature_importance"])
    print("CNN Pred Class:", assessment["cnn_prediction_class"], "| Confidence:", assessment["cnn_confidence_score"])
    print("CNN Grad-CAM path:", assessment["cnn_gradcam_path"])
    print("ANN Audio Class:", assessment["ann_prediction_class"], "| Confidence:", assessment["ann_confidence_score"])
    print("LLM Summary:", assessment["llm_summary"][:100] + "...")
    print("LLM Reasoning:", assessment["llm_reasoning"][:100] + "...")
    print("LLM Mitigation:", assessment["llm_mitigation"][:100] + "...")
except Exception as e:
    print("Failed posting assessment:", e)
    exit(1)

# Save ID for next steps
assessment_id = assessment["id"]

print("\n--- Step 3: Submitting Human-in-the-Loop Override Review ---")
hitl_payload = {
    "override_lstm_class": 0, # Force Low Risk
    "override_cnn_class": 0,  # Force Healthy
    "analyst_notes": "Acoustic signatures and vibration perturbations verified. Overrode to low risk class based on context.",
    "reviewed_by": "Lead Inspector Sharjeel"
}

try:
    res = requests.post(f"{BASE_URL}/api/assessments/{assessment_id}/hitl", data=hitl_payload)
    print("Status Code:", res.status_code)
    updated = res.json()
    print("Updated is_reviewed:", updated["is_reviewed"])
    print("Updated override_lstm_class:", updated["override_lstm_class"])
    print("Analyst Notes:", updated["analyst_notes"])
except Exception as e:
    print("Failed to submit HITL review:", e)
    exit(1)

print("\n--- Step 4: Downloading Compiled PDF Report ---")
try:
    res = requests.get(f"{BASE_URL}/api/assessments/{assessment_id}/pdf")
    print("Status Code:", res.status_code)
    print("Content-Type Header:", res.headers.get("content-type"))
    pdf_size = len(res.content)
    print("Downloaded PDF size in bytes:", pdf_size)
    if pdf_size > 1000:
        print("Success! Generated PDF contains data.")
    else:
        print("Warning: PDF size is very small, might be empty or error.")
except Exception as e:
    print("Failed to download PDF:", e)
    exit(1)

print("\nAll pipeline verification steps completed successfully!")
