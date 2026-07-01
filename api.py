from fastapi import FastAPI,HTTPException
from fastapi.responses import JSONResponse 
from pydantic import BaseModel


from rakuten_amazon_to_shopee.service import fetch_source_product
from rakuten_amazon_to_shopee.transform import source_to_listing_preview

app = FastAPI()
# uvicorn api:app --reload
# 用上面那行來啟動，最後面的 --reload 是用來 hot reload 用的

class ProductData(BaseModel): # post 傳進來的商品資訊會是以
    title: str
    price_twd: int # 若傳進來的是"580"，BaseModel 支援自動轉型成 int，不會抱錯
    description: str
    image_urls: list[str]

# ====================================================================


@app.exception_handler(Exception)
def global_excption_handler(request,exc):
    return JSONResponse(status_code=500,content={"detail":str(exc)})


@app.get("/")
def read_root():
    return {"message":"hello"}

@app.get("/product")
def get_product(url:str):
    try:
        product = fetch_source_product(url)
        preview = source_to_listing_preview(product)
        return preview.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=400,detail=str(e))

@app.post("/upload-to-shopee")
def upload_to_shopee(product:ProductData):
    pass    