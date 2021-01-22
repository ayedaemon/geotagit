from typing import List
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

import utils

app = FastAPI()
app.mount("/images", StaticFiles(directory="images"), name="images")

# @app.post("/files/")
# async def create_files(files: List[bytes] = File(...)):
#     return {"file_sizes": [file for file in files]}


@app.post("/uploadfiles/")
async def create_upload_files(files: List[UploadFile] = File(...)):
    status = await utils.is_good(files)
    status = { k.filename:v for k,v in zip(files, status)}
    def checker(x):
        nonlocal status
        if status[x] == "No Exec data":
        	return False
        else:
        	return True

    uploaded = ", ".join(filter(checker, status))
    from itertools import filterfalse
    not_uploaded = ", ".join(filterfalse(checker, status))
    return {"Uploaded": uploaded, "Not Uploaded": not_uploaded}


@app.get("/upload")
async def main():
    content = """
<body>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)


# @app.get("/refresh_db")
# def refresh_db():
#     return {"status": "Under"}

@app.get("/map")
def map():
    map_location = utils.create_map()
    with open(map_location) as f:
        html = f.read()
    return HTMLResponse(content = html)


# @app.get("/images/{fn}")
# def get_image(fn):
#     try:
#         print(fn)
#         return FileResponse(f"/images/{fn}")
#     except:
#         return None
