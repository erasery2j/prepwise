from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import engine, SessionLocal, Base
from app.models import User
from app.security import hash_password, verify_password, create_token
from app.ai_service import career_advice, interview_feedback

app = FastAPI(title="PrepWise AI")

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "PrepWise AI is running"}

@app.post("/register")
def register(email: str, password: str, db: Session = Depends(get_db)):
    user = User(email=email, password=hash_password(password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User created"}

@app.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_token({"sub": user.email})
    return {"access_token": token}

@app.post("/career-advice")
def get_career_advice(profile: str):
    return {"advice": career_advice(profile)}

@app.post("/interview-feedback")
def get_interview_feedback(answer: str):
    return {"feedback": interview_feedback(answer)}
