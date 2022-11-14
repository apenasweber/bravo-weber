from fastapi import FastAPI, status
from app.routers import currency

app = FastAPI()
app.include_router(currency.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}