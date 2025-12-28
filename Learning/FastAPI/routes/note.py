from fastapi import APIRouter,Request
from models.note import Note
from config.db import conn
from schemas.note import notesEntity, noteEntity
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

note = APIRouter()
templates = Jinja2Templates(directory="templates")


@note.get("/", response_class=HTMLResponse)
async def read_item(request: Request):  # type: ignore
    docs = conn.notes.notes.find({})
    newDocs = []
    for doc in docs:    
        newDocs.append({
            "id": doc["_id"],
            "title": doc["title"],  
        })
    return templates.TemplateResponse("index.html", {"request": request, "newDocs": newDocs})


# @note.post("/")
# def add_note(note: Note):
#     inserted_note = conn.nodes.notes.insert_one(dict(note)) # type: ignore
#     return noteEntity(inserted_note)

@note.post("/")#, response_class=HTMLResponse
async def create_item(request: Request):
    form = await request.form()
    formDict = dict(form)
    formDict["important"] = True if formDict["important"] == "on" else False  # type: ignore
    note = conn.nodes.notes.insert_one(formDict) # type: ignore
    return {"Success":True}