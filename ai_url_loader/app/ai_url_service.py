from langchain_community.document_loaders import AsyncHtmlLoader
from langchain.chains import create_extraction_chain
from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
import pprint
import os
from dotenv import load_dotenv, find_dotenv
from langchain_community.document_transformers import BeautifulSoupTransformer

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

llm = ChatOpenAI(temperature=0, model="gpt-4-turbo-preview")

def extract(content: str, schema: dict):
    return create_extraction_chain(schema=schema, llm=llm).invoke({"input": content})

def scrape_with_playwright(urls, schema):
    loader = AsyncHtmlLoader(urls)
    docs_html = loader.load()
    print("\n\n ---------- Extracted docs_html ------------\n\n", len(docs_html))
    print("Extracting content with LLM")

    bs_transformer = BeautifulSoupTransformer()
    docs_transformed = bs_transformer.transform_documents(docs_html, tags_to_extract=["span", "h1", "h2", "h3", "h4", "img"])

    print("\n\n ---------- Extracted docs_transformed ------------\n\n", len(docs_transformed))
    # print("\n\n ---------- Extracted docs_transformed ------------\n\n", docs_transformed[0])
    # # Grab the first 1000 tokens of the site
    # splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    #     chunk_size=2000, chunk_overlap=0
    # )
    # splits = splitter.split_documents(docs_transformed)

    # print("\n\n ---------- Extracted splits ------------\n\n", splits)

    # Process the first split
    print("Extracting content with LLM")
    extracted_content = extract(schema=schema, content=docs_transformed)
    pprint.pprint(extracted_content)
    return extracted_content