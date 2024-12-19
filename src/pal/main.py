import logging
from fastapi import FastAPI

from .llm import load_model
from .status import status_router
from .query import query_router

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")


app = FastAPI()

app.include_router(status_router)
app.include_router(query_router)


@app.on_event("startup")
def on_startup():
    logging.info("Starting the levers...")
    load_model()


def start():
    import uvicorn
    uvicorn.run("pal.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    start()
