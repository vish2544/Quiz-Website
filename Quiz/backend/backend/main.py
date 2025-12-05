# backend/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Text, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import uuid
import os
from ai_gen import generate_questions
import random
import json

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./quiz.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    password_hash = Column(String)
    verified = Column(Boolean, default=False)

class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"
    attempt_id = Column(String, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    language = Column(String)
    level = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="in_progress")
    # relationship will be manual

class AIGeneratedQuestion(Base):
    __tablename__ = "ai_generated_questions"
    id = Column(Integer, primary_key=True, index=True)
    attempt_id = Column(String, index=True)
    question_text = Column(Text)
    optionA = Column(String)
    optionB = Column(String)
    optionC = Column(String)
    optionD = Column(String)
    correct_option = Column(String)
    explanation = Column(Text)

class Result(Base):
    __tablename__ = "results"
    id = Column(Integer, primary_key=True, index=True)
    attempt_id = Column(String, index=True)
    score = Column(Integer)
    total_questions = Column(Integer)
    correct_answers = Column(Integer)
    time_taken = Column(Integer)  # seconds
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Quiz Start Module")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# helper to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/generate-questions")
def generate_questions_endpoint(payload: dict):
    """
    Input: {"language": "Python", "level": "Beginner", "user_id": 1, "n": 10}
    Action: Call AI -> generate questions, randomize options, store temp and return attempt_id + questions
    """
    language = payload.get("language")
    level = payload.get("level")
    user_id = payload.get("user_id", 0)
    n = int(payload.get("n", 10))

    if not language or not level:
        raise HTTPException(status_code=400, detail="language and level required")

    # Generate via AI generator
    qlist = generate_questions(language, level, n=n)

    # create attempt id
    attempt_id = str(uuid.uuid4())

    # store in DB
    db = next(get_db())
    attempt = QuizAttempt(attempt_id=attempt_id, user_id=user_id, language=language, level=level)
    db.add(attempt)
    db.commit()

    # For each question, shuffle options and store as A/B/C/D
    for q in qlist:
        options = q.get("options") if isinstance(q.get("options"), list) else []
        if len(options) < 4:
            # pad options
            options = (options + ["OptionX", "OptionY", "OptionZ", "OptionW"])[:4]
        random.shuffle(options)
        correct = q.get("correct_option")
        # if correct is the text of option, keep it; else assume first original option is correct -> try to find match
        if correct not in options:
            # naive: set first option as correct
            correct = options[0]
        qrow = AIGeneratedQuestion(
            attempt_id=attempt_id,
            question_text=q.get("question_text"),
            optionA=options[0],
            optionB=options[1],
            optionC=options[2],
            optionD=options[3],
            correct_option=correct,
            explanation=q.get("explanation") or ""
        )
        db.add(qrow)
    db.commit()

    # Return questions (without revealing correct_option) shuffled
    questions_for_client = []
    rows = db.query(AIGeneratedQuestion).filter(AIGeneratedQuestion.attempt_id == attempt_id).all()
    for r in rows:
        questions_for_client.append({
            "id": r.id,
            "question_text": r.question_text,
            "options": [r.optionA, r.optionB, r.optionC, r.optionD]
        })

    # randomize question order for this attempt
    random.shuffle(questions_for_client)

    return {"attempt_id": attempt_id, "questions": questions_for_client}

@app.post("/start-quiz")
def start_quiz(payload: dict):
    """Alias for generate_questions to match spec; can be extended"""
    return generate_questions_endpoint(payload)

@app.post("/submit-quiz")
def submit_quiz(payload: dict):
    """
    Input: {"attempt_id": "<id>", "responses": [{"question_id": id, "selected": "Option text", "time_spent": seconds}, ...]}
    Action: evaluate & store result
    """
    attempt_id = payload.get("attempt_id")
    responses = payload.get("responses", [])
    if not attempt_id:
        raise HTTPException(status_code=400, detail="attempt_id required")

    db = next(get_db())
    rows = db.query(AIGeneratedQuestion).filter(AIGeneratedQuestion.attempt_id == attempt_id).all()
    if not rows:
        raise HTTPException(status_code=404, detail="attempt not found")

    qmap = {r.id: r for r in rows}
    total = len(rows)
    correct = 0
    for resp in responses:
        qid = resp.get("question_id")
        selected = resp.get("selected")
        q = qmap.get(qid)
        if q and selected == q.correct_option:
            correct += 1

    score = int((correct / total) * 100) if total > 0 else 0
    # store result
    time_taken = payload.get("time_taken", 0)
    res = Result(attempt_id=attempt_id, score=score, total_questions=total, correct_answers=correct, time_taken=time_taken)
    db.add(res)
    # mark attempt status
    attempt = db.query(QuizAttempt).filter(QuizAttempt.attempt_id == attempt_id).first()
    if attempt:
        attempt.status = "completed"
        db.add(attempt)
    db.commit()

    return {"attempt_id": attempt_id, "score": score, "total": total, "correct": correct}

@app.get("/quiz-results/{attempt_id}")
def quiz_results(attempt_id: str):
    db = next(get_db())
    res = db.query(Result).filter(Result.attempt_id == attempt_id).first()
    if not res:
        raise HTTPException(status_code=404, detail="result not found")
    # also return question-by-question correctness
    rows = db.query(AIGeneratedQuestion).filter(AIGeneratedQuestion.attempt_id == attempt_id).all()
    qlist = []
    for r in rows:
        qlist.append({
            "id": r.id,
            "question_text": r.question_text,
            "options": [r.optionA, r.optionB, r.optionC, r.optionD],
            "correct_option": r.correct_option,
            "explanation": r.explanation
        })
    return {
        "attempt_id": attempt_id,
        "score": res.score,
        "total_questions": res.total_questions,
        "correct_answers": res.correct_answers,
        "time_taken": res.time_taken,
        "questions": qlist
    }
