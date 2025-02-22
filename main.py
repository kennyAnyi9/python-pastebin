from fastapi import FastAPI, HTTPException, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
import uuid
from db import PasteDB, SessionLocal, engine

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("create.html", {"request": request})

@app.post("/create", response_class=HTMLResponse)
def create_paste(request: Request, content: str = Form(...), db: Session = Depends(get_db)):
    paste_id = str(uuid.uuid4())[:8]  # Shorten to 8 characters for simplicity
    db_paste = PasteDB(id=paste_id, content=content)
    db.add(db_paste)
    db.commit()
    # Get the host URL from the request
    host_url = request.url.hostname or "127.0.0.1:8000"
    full_url = f"http://{host_url}/{paste_id}"
    return templates.TemplateResponse("view.html", {"request": request, "content": content, "url": full_url})

@app.get("/{paste_id}", response_class=HTMLResponse)
def get_paste(request: Request, paste_id: str, db: Session = Depends(get_db)):
    paste = db.query(PasteDB).filter(PasteDB.id == paste_id).first()
    if paste is None:
        raise HTTPException(status_code=404, detail="Paste not found")
    host_url = request.url.hostname or "127.0.0.1:8000"
    full_url = f"http://{host_url}/{paste_id}"
    return templates.TemplateResponse("view.html", {"request": request, "content": paste.content, "url": full_url})