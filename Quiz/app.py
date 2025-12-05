from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import get_db, Base, engine
from models import User, OTP
from otp_utils import generate_unique_otp, hash_otp, otp_expiry
import smtplib
import os
import requests

Base.metadata.create_all(bind=engine)
app = FastAPI()

EMAILJS_SERVICE_ID = "Programmers Quiz"
EMAILJS_TEMPLATE_ID = "template_2ugk8ja"
EMAILJS_PUBLIC_KEY = "j0o722bDH7FxNRVJN"

@app.post("/register")
async def register_user(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if db.query(User).filter(User.email==email).first():
        return JSONResponse({"error": "Email already registered"}, status_code=400)

    # Hash password
    password_hash = hash_otp(password)  # reuse OTP hash function for simplicity

    # Create user
    user = User(name=name, email=email, password_hash=password_hash)
    db.add(user)
    db.commit()
    db.refresh(user)

    # Generate OTP
    otp_plain = generate_unique_otp()
    otp_hashed = hash_otp(otp_plain)
    expiry = otp_expiry()

    otp_entry = OTP(email=email, otp_hash=otp_hashed, expires_at=expiry)
    db.add(otp_entry)
    db.commit()

    # Send OTP via EmailJS
    payload = {
        "service_id": EMAILJS_SERVICE_ID,
        "template_id": EMAILJS_TEMPLATE_ID,
        "user_id": EMAILJS_PUBLIC_KEY,
        "template_params": {
            "to_email": email,
            "otp_code": otp_plain
        }
    }
    requests.post("https://api.emailjs.com/api/v1.0/email/send", json=payload)

    return {"message": "User registered successfully. OTP sent to email."}
