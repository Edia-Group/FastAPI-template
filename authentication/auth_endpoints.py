from datetime import datetime, timezone
from sqlalchemy.orm import Session
import authentication.auth_service as auth_service
from database import get_db
from models import OTP
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import schemas

authentication_router = APIRouter(prefix="/auth", tags=["Authentication"])

@authentication_router.post("/verify-token")
async def verify_token(verify_token: schemas.VerifyToken, db: Session = Depends(get_db)):
    token = auth_service.verify_otp(verify_token.phone_number, verify_token.otp, db)
    return {"access_token": token, "token_type": "bearer"}

@authentication_router.post("/send-otp")
async def request_otp(phone_number: schemas.PhoneRequest, db: Session = Depends(get_db)):
    phone_number = phone_number.phone_number
    otp = auth_service.generate_otp()
    existing_otp = db.query(OTP).filter(OTP.phone_number == phone_number).first() 
    
    if existing_otp: # if there is an existing otp/phone record on DB, we update the existing one
        existing_otp.otp = otp
        existing_otp.timestamp = datetime.now(timezone.utc)

    else: # if there is no existing otp/phone record on DB, we create
        print('crating otp . .. ')
        new_otp = OTP(phone_number=phone_number, otp=otp, timestamp=datetime.now(timezone.utc))
        db.add(new_otp)
    db.commit()
    otp = auth_service.send_sms(phone_number, otp)
    return {"message": f"OTP sent {otp}"} # JUST FOR TESTING, WE NEED A PROVIDER TO ACTUALLY SEND OTP



