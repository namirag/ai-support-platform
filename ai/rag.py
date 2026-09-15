import os

import chromadb
from dotenv import load_dotenv
from openai import OpenAI

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

chroma_client = chromadb.PersistentClient(path=os.path.join(BASE_DIR, "chroma_db"))

collection = chroma_client.get_or_create_collection(name="support_documents")


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50):
    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap

    return chunks


def create_embedding(text: str):
    response = client.embeddings.create(model="text-embedding-3-small", input=text)

    return response.data[0].embedding


def add_document(document_id: str, text: str):
    chunks = chunk_text(text)

    embeddings = [create_embedding(chunk) for chunk in chunks]

    ids = [f"{document_id}_{index}" for index in range(len(chunks))]

    collection.add(ids=ids, documents=chunks, embeddings=embeddings)

    return len(chunks)


def search_documents(query: str, top_k: int = 3):
    query_embedding = create_embedding(query)

    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)

    return results["documents"][0]


def generate_answer(question: str):
    relevant_chunks = search_documents(question, top_k=5)

    context = "\n\n".join(relevant_chunks)

    prompt = f"""
Answer the customer's question using only the information provided in the context.

Context:
{context}

Customer question:
{question}

If the answer is not available in the context, say that you do not have enough information to answer.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful customer support assistant.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0,
    )

    return response.choices[0].message.content
