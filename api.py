from fastapi import FastAPI

app = FastAPI()
# uvicorn api:app --reload
# 用上面那行來啟動，最後面的 --reload 是用來hot reload 用的



@app.get("/")
def read_root():
    return {"message":"hello"}

@app.get("/product")
def get_product(url:str):
    print(url)