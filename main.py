# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import Base, engine, get_db
from sqlalchemy import Column, String, Integer, DateTime, Enum
from datetime import datetime

# Initialize the FastAPI application
app = FastAPI()

# Define the Appointment model
class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True)
    patient_name = Column(String)
    doctor_name = Column(String)
    department = Column(String)
    date = Column(DateTime)
    time = Column(DateTime)
    status = Column(String)

# Define the User model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    password = Column(String)

# Define the LoginRequest model
class LoginRequest(BaseModel):
    email: str
    password: str

# Define the RegisterRequest model
class RegisterRequest(BaseModel):
    email: str
    password: str

# Define the AppointmentRequest model
class AppointmentRequest(BaseModel):
    patient_name: str
    doctor_name: str
    department: str
    date: str
    time: str

# Define the AppointmentResponse model
class AppointmentResponse(BaseModel):
    id: int
    patient_name: str
    doctor_name: str
    department: str
    date: str
    time: str
    status: str

# Root route
@app.get("/")
def root():
    return {"status": "running", "docs": "/docs"}

# Health route
@app.get("/health")
def health():
    return {"status": "healthy"}

# Login endpoint
@app.post("/api/v1/auth/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user or user.password != request.password:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return {"token": "sample_token"}

# Register endpoint
@app.post("/api/v1/auth/register")
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    user = User(email=request.email, password=request.password)
    db.add(user)
    db.commit()
    return {"message": "User created successfully"}

# Create appointment endpoint
@app.post("/api/v1/appointments")
def create_appointment(request: AppointmentRequest, db: Session = Depends(get_db)):
    appointment = Appointment(
        patient_name=request.patient_name,
        doctor_name=request.doctor_name,
        department=request.department,
        date=datetime.strptime(request.date, "%Y-%m-%d"),
        time=datetime.strptime(request.time, "%H:%M"),
        status="Scheduled"
    )
    db.add(appointment)
    db.commit()
    return {"message": "Appointment created successfully"}

# Get all appointments endpoint
@app.get("/api/v1/appointments")
def get_appointments(db: Session = Depends(get_db)):
    appointments = db.query(Appointment).all()
    return [AppointmentResponse(
        id=appointment.id,
        patient_name=appointment.patient_name,
        doctor_name=appointment.doctor_name,
        department=appointment.department,
        date=appointment.date.strftime("%Y-%m-%d"),
        time=appointment.time.strftime("%H:%M"),
        status=appointment.status
    ) for appointment in appointments]

# Get appointment by id endpoint
@app.get("/api/v1/appointments/{appointment_id}")
def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return AppointmentResponse(
        id=appointment.id,
        patient_name=appointment.patient_name,
        doctor_name=appointment.doctor_name,
        department=appointment.department,
        date=appointment.date.strftime("%Y-%m-%d"),
        time=appointment.time.strftime("%H:%M"),
        status=appointment.status
    )

# Update appointment endpoint
@app.put("/api/v1/appointments/{appointment_id}")
def update_appointment(appointment_id: int, request: AppointmentRequest, db: Session = Depends(get_db)):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    appointment.patient_name = request.patient_name
    appointment.doctor_name = request.doctor_name
    appointment.department = request.department
    appointment.date = datetime.strptime(request.date, "%Y-%m-%d")
    appointment.time = datetime.strptime(request.time, "%H:%M")
    db.commit()
    return {"message": "Appointment updated successfully"}

# Delete appointment endpoint
@app.delete("/api/v1/appointments/{appointment_id}")
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    db.delete(appointment)
    db.commit()
    return {"message": "Appointment deleted successfully"}