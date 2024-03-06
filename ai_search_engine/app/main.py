from fastapi import FastAPI, HTTPException
from .ai_search_engine import search

app = FastAPI()

@app.get("/health/api", tags=["Health"])
async def api_root():
    return {"message": "API is up and running!"}


@app.get("/ai-search")
def search_web(prompt: str):
    try:
        data = search(prompt)
        print(f"\n ---- \n ----- data: {data} ---- \n")
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
#     return search(prompt)