from fastapi import FastAPI

app = FastAPI(title="AI Customer Support Platform")


@app.get("/")
def root():
    return {"message": "AI Customer Support Platform API is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}
