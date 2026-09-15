from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from backend.database import Base, engine, SessionLocal
from backend.models import User, Conversation, Message
from backend.schemas import UserCreate, ConversationCreate, MessageCreate, ChatRequest

from ai.rag import generate_answer

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
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    user = User(name=user_data.name, email=user_data.email)
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@app.post("/conversations")
def create_conversation(
    conversation_data: ConversationCreate, db: Session = Depends(get_db)
):
    conversation = Conversation(
        user_id=conversation_data.user_id, title=conversation_data.title
    )

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return conversation


@app.post("/messages")
def create_message(message_data: MessageCreate, db: Session = Depends(get_db)):
    message = Message(
        conversation_id=message_data.conversation_id,
        sender=message_data.sender,
        content=message_data.content,
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    return message


@app.post("/chat")
def chat(chat_data: ChatRequest):
    answer = generate_answer(chat_data.question)

    return {"question": chat_data.question, "answer": answer}
