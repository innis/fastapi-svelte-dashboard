from fastapi import APIRouter, Request
from typing import Optional
from fastapi.templating import Jinja2Templates

router = APIRouter()


templates = Jinja2Templates(directory="admin-app/public")
#templates.env.globals["STATIC_URL"] = "/static"

@router.get("/")
@router.get("/{q}")
async def index(request: Request):
    return templates.TemplateResponse("index.html", context={"request": request})