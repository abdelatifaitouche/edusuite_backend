from fastapi import FastAPI


app = FastAPI()


@app.get("/")
def routes():
    return "hello edusuite"
