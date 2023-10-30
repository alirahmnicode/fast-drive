from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from sql.database import engine
from sql import models
from routers import users, foolders, files


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(foolders.router, tags=["foolders"])
app.include_router(files.router, prefix="/files", tags=["files"])


@app.get("/")
async def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)
