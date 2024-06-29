from app.routers import crypto
from fastapi import FastAPI


app = FastAPI()

app.include_router(crypto.router)


@app.get("/")
def main():
    return {"message":"Server has started"}
