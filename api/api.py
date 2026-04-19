# from urllib import response

from fastapi import FastAPI ,UploadFile, File

import os

from agent.rag import upload_to_vector_db

from agent.agent import run_agent 

from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str

app = FastAPI()
    
    
@app.get("/")
def home():
    return {"message" : "welcome to FastAPI."}

@app.post("/chat")
def chat(request: ChatRequest):
    response = run_agent(request.message)
    return {"response": response}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    os.makedirs("uploads", exist_ok=True)

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as f:
        f.write(await file.read())

    result = upload_to_vector_db(file_path)

    return {"message": result}
