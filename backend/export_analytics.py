import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

import pandas as pd

from backend.database import SessionLocal
from backend.models import Message, Feedback

db = SessionLocal()

messages = db.query(Message).all()
feedback = db.query(Feedback).all()

message_data = [
    {
        "message_id": message.id,
        "conversation_id": message.conversation_id,
        "sender": message.sender,
        "content": message.content,
    }
    for message in messages
]

feedback_data = [
    {
        "message_id": item.message_id,
        "rating": item.rating,
        "comment": item.comment,
    }
    for item in feedback
]

messages_df = pd.DataFrame(message_data)
feedback_df = pd.DataFrame(feedback_data)

analytics_df = messages_df.merge(feedback_df, on="message_id", how="left")

output_path = os.path.join(PROJECT_ROOT, "tableau_support_analytics.csv")

analytics_df.to_csv(output_path, index=False)

db.close()

print("Tableau analytics data exported successfully.")
print(f"Rows exported: {len(analytics_df)}")
print(f"File: {output_path}")
