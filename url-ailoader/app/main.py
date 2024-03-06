from fastapi import FastAPI, HTTPException
from .ai_url_service import schema, scrape_with_playwright
from .model import ProductScrapedBase

app = FastAPI()

@app.get("/health/api", tags=["Health"])
async def api_root():
    return {"message": "URL AI Loader API is up and running!"}

@app.get("/ai_url", tags=["URL Loader"], response_model=ProductScrapedBase)
async def load_and_transform_api(url: str):
    try:
        urls = [url]
        extracted_content = scrape_with_playwright(urls, schema)
        print("\n--------------- \n extracted_content \n ---------------\n", extracted_content)

        product_metadata = extracted_content["text"][0]
        product_metadata['product_url'] = url
        return product_metadata
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))