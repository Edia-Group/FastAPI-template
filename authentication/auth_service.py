from datetime import datetime, timedelta, timezone
from authentication.auth_utils import OTP_EXPIRATION_MINUTES, ALGORITHM, SECRET_KEY, create_access_token
import jwt
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
import secrets
from models import OTP, User
from database import get_db


def send_sms(phone_number: str, otp: str):
    print(f"Sending OTP {otp} to {phone_number}")
    return otp

# JUST MOCK, WE NEED TO CHANGE WITH AN ACTUAL OTP SENDING SERVICE
def generate_otp():
    return str(secrets.randbelow(10000)).zfill(4)

def get_user_from_token(token: str, db: Session = Depends(get_db)):
    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        phone_number: str = payload.get("phone_user")
        if phone_number is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        user = db.query(User).filter(User.phone_number == phone_number).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


def verify_otp(phone_number: str, otp: str, db: Session = Depends(get_db)):

    stored_otp = db.query(OTP).filter(OTP.phone_number == phone_number).first()
    if not stored_otp:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="OTP not requested or expired")
    if stored_otp.otp != otp:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid OTP")
    if datetime.now(timezone.utc) - stored_otp.timestamp.replace(tzinfo=timezone.utc) > timedelta(minutes=OTP_EXPIRATION_MINUTES):
        db.delete(stored_otp)
        db.commit()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="OTP expired")

    # CREATE USER IF NOT EXISTS
    user = db.query(User).filter(User.phone_number == phone_number).first()
    if not user:
        user = User(phone_number=phone_number)
        db.add(user)
        db.commit()
        db.refresh(user)

    # ONCE USED WE CAN DELETE OTP
    db.delete(stored_otp)
    db.commit()
    return create_access_token({"phone_user": phone_number})