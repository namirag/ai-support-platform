from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    email: str


class ConversationCreate(BaseModel):
    user_id: int
    title: str | None = None


class MessageCreate(BaseModel):
    conversation_id: int
    sender: str
    content: str


class ChatRequest(BaseModel):
    conversation_id: int
    question: str


class FeedbackCreate(BaseModel):
    message_id: int
    rating: int
    comment: str | None = None
