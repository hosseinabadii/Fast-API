from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["Index"])


@router.get("/")
def index():
    index_content = """
    <html>
    <head>
        <title>Home</title>
    </head>
    <body>
        <h1>Welcome to My Hotel API</h1>
        <p>See the Swagger UI to test it.</p>
        <a href="http://127.0.0.1:8000/docs">click here</a>
    </body>
    </html>
    """
    return HTMLResponse(index_content)
