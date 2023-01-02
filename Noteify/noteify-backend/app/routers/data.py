from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from pathlib import Path
from fastapi.responses import FileResponse
from os import listdir
import os
from os.path import isfile, join
import json

router = APIRouter(prefix="/data", tags=["Get data"])


@router.get("/file/{filename}")
def get_file(filename: str):
    mypath = os.path.abspath(join("path", sub))
    filepath = Path(
        "png-transparent-blockchain-business-bitcoin-technology-supply-chain-management-business-people-innovation-symmetry.png"
    )
    print(filepath.resolve())
    print(filepath.name)
    # headers = {"Content-Disposition": "inline; filename={}".format(filepath.name)}
    # print(headers)
    result = [
        os.path.join(dp, f)
        for dp, dn, filenames in os.walk(PATH)
        for f in filenames
        if os.path.splitext(f)[1] in [".jpg", ".png"]
    ]
    if filename in result:
        matching = [s for s in xs if "abc" in s]
        return FileResponse(filepath.resolve(), filename=filepath.name)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )


@router.get("/filename/{sub}")
def get_filename(sub: str):
    mypath = os.path.abspath(join(*["app", "data", sub]))
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    print(onlyfiles)
    return Response(content=json.dumps(onlyfiles), media_type="application/json")
