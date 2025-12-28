import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

conn = MongoClient("mongodb://localhost:27017/")

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request): # type: ignore
    docs = conn.notes.notes.find({})
    newDocs=[]
    for doc in docs:
        newDocs.append({
            "id":doc["_id"],
            "note":doc["note"],
        })
        print(doc["_id"])  # Convert cursor to list to pass into template
    return templates.TemplateResponse(r"index.html", {"request": request, "newDocs":newDocs})


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):  # OK if Python 3.10+
    return {"item_id": item_id, "q": q}

