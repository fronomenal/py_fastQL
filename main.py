import os

import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv(".env")

app = FastAPI()

@app.get("/testing")
async def root():
    return {"message": os.getenv("TESTING")}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)