from langchain_community.document_loaders import AsyncHtmlLoader
from langchain.chains import create_extraction_chain
from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
import pprint
import os
from dotenv import load_dotenv, find_dotenv

_: bool = load_dotenv(find_dotenv())

schema = {
    "properties": {
        "product_id": {"type": "string"},
        "product_title": {"type": "string"},
        "company_name": {"type": "string"},
        "price": {"type": "string"},
        "currency": {"type": "string"},
        "image_url": {"type": "array", "items": {"type": "string"}},
        "product_url": {"type": "string"},
        "manufacturing_materials": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["product_id", "product_title", "company_name", "price", "currency", "image_url", "product_url", "manufacturing_material"],
}

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")

def extract(content: str, schema: dict):
    return create_extraction_chain(schema=schema, llm=llm).invoke(content)

def scrape_with_playwright(urls, schema):
    loader = AsyncHtmlLoader(urls)
    docs = loader.load()
    print("Extracting content with LLM")

    # Grab the first 1000 tokens of the site
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=1000, chunk_overlap=0
    )
    splits = splitter.split_documents(docs)

    # Process the first split
    extracted_content = extract(schema=schema, content=splits[0].page_content)
    pprint.pprint(extracted_content)
    return extracted_content