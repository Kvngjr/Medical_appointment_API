from fastapi import FastAPI, Body, HTTPException, status
from pydantic import ValidationError

from models import Patient, Doctor

patients = {}
appointments = {}
doctors = {}

app = FastAPI()


@app.get("/home")
def home():
    return {"message": "Hello World"}


@app.post("/patients", status_code=status.HTTP_201_CREATED)
async def create_patient(patient: Patient):
    # Validate data
    try:
        patient = Patient(**patient.model_dump())
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        )

    # Assign unique ID Patients
    patient.id = len(patients) + 1
    patients[patient.id] = patient
    return patient


@app.post("/doctors", status_code=status.HTTP_201_CREATED)
async def create_doctor(doctor: Doctor):
    try:
        doctor = Doctor(**doctor.model_dump())
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        )

    doctor.id = len(doctors) + 1
    doctors[doctor.id] = doctor
    return doctor


@app.get("/patients/{patient_id}")
async def get_patient(patient_id: int):
    if patient_id not in patients:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found"
        )
    return patients[patient_id]


@app.get("/doctors/{doctor_id}")
async def get_doctor(doctor_id: int):
    if doctor_id not in doctors:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found"
        )
    return doctors[doctor_id]


@app.put("/patients/{patient_id}")
async def update_patient(patient_id: int, updated_data: Patient):
    if patient_id not in patients:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found"
        )

    # Update patient data
    patients[patient_id] = updated_data.model_copy(update=patients[patient_id].dict())
    return patients[patient_id]


@app.put("/doctors/{doctor_id}")
async def update_doctor(doctor_id: int, updated_data: Doctor):
    if doctor_id not in doctors:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found"
        )

    doctors[doctor_id] = updated_data.model_copy(update=doctors[doctor_id].dict())
    return doctors[doctor_id]


@app.delete("/patients/{patient_id}")
async def delete_patient(patient_id: int):
    if patient_id not in patients:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found"
        )

    # Delete appointments associated with the patient
    for appointment_id, appointment in appointments.items():
        if appointment.patient.id == patient_id:
            del appointments[appointment_id]

    del patients[patient_id]
    return {"message": "Patient deleted successfully"}


@app.delete("/doctors/{doctor_id}")
async def delete_doctor(doctor_id: int):
    if doctor_id not in doctors:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found"
        )

    # Delete appointments associated
