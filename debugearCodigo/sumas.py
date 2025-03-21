from fastapi import FastAPI
from uvicorn import run

app = FastAPI()

@app.get("/")
def read_root():
    a = "a"
    b = "b" + a
    return {"Hello": "World", "b": b}

# Asegúrate de tener el router 'user' definido antes de incluirlo
# from routes.user import user
# app.include_router(user)

if __name__ == "__main__":
    run(app, host="127.0.0.1", port=8000)