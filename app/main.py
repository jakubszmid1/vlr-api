from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import uvicorn
from api.routes import router

app = FastAPI(
    title="VLR Web Scraping API",
    description="An API for scraping data from VLR.gg",
)

app.include_router(router)

@app.get("/")
def root():
    return RedirectResponse(url="/docs")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=3001)