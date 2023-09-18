from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import role_listing

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(role_listing.router)

@app.get("/test")
def test():
    return {"message": "Test"}