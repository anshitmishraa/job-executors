from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from backend.main import app as api_app

app = FastAPI()

# Mount the static files directory
app.mount("/frontend", StaticFiles(directory="./frontend"), name="frontend")
templates = Jinja2Templates(directory="./frontend")


@app.get("/")
async def home(request: Request):
    """
    Handler for the home route.

    Args:
        request (Request): The incoming request object.

    Returns:
        TemplateResponse: The rendered HTML template response.

    Comments:
        This handler serves as the entry point for the home route ("/").
        It renders the "index.html" template and passes the request context to it.
    """
    context = {"request": request}
    return templates.TemplateResponse("index.html", context=context)

# Include the API routes from api/main.py
app.include_router(api_app.router)
