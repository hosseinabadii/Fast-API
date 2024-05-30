from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["Index"])


@router.get("/")
def index() -> HTMLResponse:
    content = """
    <h1>Welcome to my API</h1>
    <p>Please check the <a href="http://127.0.0.1:8000/docs">documentation</a> page.</p>
    """
    return HTMLResponse(content)
