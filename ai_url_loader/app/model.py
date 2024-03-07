from pydantic import BaseModel

class ProductScrapedBase(BaseModel):
    product_id: str
    product_title: str
    company_name: str
    price: str
    currency: str
    image_url: list[str]
    product_url: str
    manufacturing_materials: list[str]