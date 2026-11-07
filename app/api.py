
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

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
def search_endpoint(
    query: str,
    source: str = "wikipedia",
    limit: int = 20,
):
    try:
        if limit < 1 or limit > 50:
            raise HTTPException(
                status_code=400,
                detail="Limit must be between 1 and 50.",
            )

        results = search(
            query,
            source,
            limit=limit,
        )

        return {
            "results": results,
            "total_results": len(results),
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )
