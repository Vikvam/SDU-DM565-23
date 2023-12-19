import uvicorn
from fastapi import FastAPI, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from starlette.responses import JSONResponse

from backend.config import get_settings
from backend.google_api.google_route_finder import GoogleRouteFinder

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

google_finder = GoogleRouteFinder(get_settings().google_maps_api_key)


def get_google_finder():
    return google_finder


class SearchData(BaseModel):
    from_name: str
    to_name: str
    departure_datetime: str


@app.post("/search")
async def search(search_data: SearchData, finder=Depends(get_google_finder)):
    result = finder.find_routes(search_data.from_name, search_data.to_name, search_data.departure_datetime)
    json_result = jsonable_encoder(result)

    return JSONResponse(content=json_result)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
