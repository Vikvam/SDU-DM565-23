import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SearchData(BaseModel):
    from_name: str
    to_name: str
    departure: str


@app.post("/search")
async def search(search_data: SearchData):
    # print(from_name, to_name, departure)
    print(search_data)

    return {"i": "am", "a": "response"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)