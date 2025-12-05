import random, string, bcrypt
from datetime import datetime, timedelta

def generate_unique_otp(length=6):
    """Generate unique alphanumeric OTP"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def hash_otp(otp):
    return bcrypt.hashpw(otp.encode(), bcrypt.gensalt()).decode()

def verify_otp(plain_otp, hashed_otp):
    return bcrypt.checkpw(plain_otp.encode(), hashed_otp.encode())

def otp_expiry(minutes=5):
    return datetime.utcnow() + timedelta(minutes=minutes)