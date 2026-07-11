import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_and_get_student(client: AsyncClient):
    # 1. Register a new student
    student_payload = {
        "student_code": "GP-999",
        "first_name": "Test",
        "last_name": "Student",
        "age": 16,
        "gender": "F",
        "school": "GP"
    }
    
    response = await client.post("/api/v1/students", json=student_payload)
    assert response.status_code == 201
    data = response.json()
    assert data["student_code"] == "GP-999"
    assert data["first_name"] == "Test"
    student_id = data["id"]
    
    # 2. Get students registry
    response = await client.get("/api/v1/students")
    assert response.status_code == 200
    students_list = response.json()
    assert len(students_list) >= 1
    assert any(s["id"] == student_id for s in students_list)
    
    # 3. Get single student details
    response = await client.get(f"/api/v1/students/{student_id}")
    assert response.status_code == 200
    assert response.json()["student_code"] == "GP-999"

@pytest.mark.asyncio
async def test_add_academic_record(client: AsyncClient):
    # 1. Create a student first
    student_payload = {
        "student_code": "MS-999",
        "first_name": "John",
        "last_name": "Doe",
        "age": 17,
        "gender": "M",
        "school": "MS"
    }
    response = await client.post("/api/v1/students", json=student_payload)
    student_id = response.json()["id"]
    
    # 2. Add an academic record
    record_payload = {
        "study_time": 3,
        "failures": 1,
        "absences": 5,
        "family_support": "yes",
        "school_support": "no",
        "internet_access": "yes",
        "health": 5,
        "g1": 14.5,
        "g2": 15.0
    }
    response = await client.post(f"/api/v1/students/{student_id}/records", json=record_payload)
    assert response.status_code == 201
    record_data = response.json()
    assert record_data["failures"] == 1
    assert record_data["g1"] == 14.5
    
    # 3. Get academic records
    response = await client.get(f"/api/v1/students/{student_id}/records")
    assert response.status_code == 200
    records_list = response.json()
    assert len(records_list) == 1
    assert records_list[0]["failures"] == 1
