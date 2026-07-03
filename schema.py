from pydantic import BaseModel

class ProductData(BaseModel):
    title: str
    price_twd: int # 若傳進來的是"580"，BaseModel 支援自動轉型成 int，不會抱錯
    description: str
    image_urls: list[str]