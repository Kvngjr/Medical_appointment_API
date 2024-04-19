from pydantic import BaseModel, ValidationError

class Patient(BaseModel):
    id: int
    name: str
    age: int
    sex: str
    weight: float
    height: float
    phone: str

class Doctor(BaseModel):
    id: int
    name: str
    specialization: str
    phone: str
    is_available: bool = True

class Appointment(BaseModel):
    id: int
    patient: Patient
    doctor: Doctor
    date: str
