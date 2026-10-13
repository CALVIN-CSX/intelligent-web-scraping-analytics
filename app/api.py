from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException

from app.search import search

app = FastAPI()

origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/search")
def search_endpoint(query: str, source: str = "wikipedia"):
    try:
        results = search(query, source)
        return {"results": results}
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )