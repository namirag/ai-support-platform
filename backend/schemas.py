from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    email: str


class ConversationCreate(BaseModel):
    user_id: int
    title: str | None = None
