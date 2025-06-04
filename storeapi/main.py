from fastapi import FastAPI

app = FastAPI()


@app.get("/")  # api.com/
async def root():
    return {"message": "Hello, world!"}