import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_student_risk_prediction(client: AsyncClient):
    # 1. Create a student
    student_payload = {
        "student_code": "GP-444",
        "first_name": "Anna",
        "last_name": "Smith",
        "age": 15,
        "gender": "F",
        "school": "GP"
    }
    response = await client.post("/api/v1/students", json=student_payload)
    student_id = response.json()["id"]
    
    # 2. Add an academic record
    record_payload = {
        "study_time": 2,
        "failures": 0,
        "absences": 4,
        "family_support": "yes",
        "school_support": "no",
        "internet_access": "yes",
        "health": 3,
        "g1": 12.0,
        "g2": 11.0
    }
    await client.post(f"/api/v1/students/{student_id}/records", json=record_payload)
    
    # 3. Request model prediction (LATE_STAGE)
    response = await client.post(f"/api/v1/students/{student_id}/predict?model_type=LATE_STAGE")
    assert response.status_code == 200
    prediction = response.json()
    assert "risk_level" in prediction
    assert "confidence" in prediction
    assert "shap_values" in prediction
    assert "risk_factors" in prediction
    assert "protective_factors" in prediction
    
    # 4. Get student predictions list
    response = await client.get(f"/api/v1/students/{student_id}/predictions")
    assert response.status_code == 200
    predictions_list = response.json()
    assert len(predictions_list) == 1
    assert predictions_list[0]["id"] == prediction["id"]
