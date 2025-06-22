from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message":"Hello,World"}

@app.get("/items/{item_id}")
def rad_item(item_id:int):
    return {"item_id": item_id}

@app.get("/items/")
def read_items(skip=0,limit=1):    
    return{"skip":skip,"limit":limit}
