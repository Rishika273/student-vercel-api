from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import json, os

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Load student data
data_path = os.path.join(os.path.dirname(__file__), "marks-data.json")
with open(data_path) as f:
    students = json.load(f)

@app.get("/api")
async def get_marks(name: List[str] = Query(None)):
    if not name:
        return {"error": "Please provide at least one name"}
    results = [
        next((s["marks"] for s in students if s["name"].lower() == n.lower()), None)
        for n in name
    ]
    return {"marks": results}

@app.get("/")
async def root():
    return {"message": "Use /api?name=Alice&name=Bob to get student marks"}

# Optional: Local testing
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("index:app", host="0.0.0.0", port=8000, reload=True)
