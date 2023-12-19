import uvicorn
from fastapi import FastAPI, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from scrapy.crawler import CrawlerProcess
from starlette.responses import JSONResponse

from backend.config import get_settings, get_pipeline_crawler_process_settings
from backend.google_api.google_route_finder import GoogleRouteFinder
from backend.name_resolvers.openstreet_name_resolver import OpenStreetMapNameResolver
from backend.route_finder.route_finder import RouteFinder

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

route_finder = RouteFinder(
    GoogleRouteFinder(get_settings().google_maps_api_key),
    CrawlerProcess(get_pipeline_crawler_process_settings()),
    [OpenStreetMapNameResolver()]
)
get_route_finder = lambda: route_finder


class SearchData(BaseModel):
    from_name: str
    to_name: str
    departure: str


@app.post("/search")
async def search(search_data: SearchData, route_finder=Depends(get_route_finder)):
    result = route_finder.find_routes(search_data.from_name, search_data.to_name, search_data.departure)
    json_result = jsonable_encoder(result)
    return JSONResponse(content=json_result)


@app.get("/search_example")
async def search(route_finder=Depends(get_route_finder)):
    result = route_finder.find_routes("Berlin", "Munich", "2024-01-31T00:00:00Z")
    json_result = jsonable_encoder(result)
    return JSONResponse(content={})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
