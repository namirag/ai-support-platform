from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import Base, engine, SessionLocal
from models import User

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Customer Support Platform")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "AI Customer Support Platform API is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/users")
def create_user(name: str, email: str, db: Session = Depends(get_db)):
    user = User(name=name, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)

    return user
