from fastapi import FastAPI
from quotes.router import router as quotes_router

app = FastAPI()

routers = (quotes_router,)
for router in routers:
    app.include_router(router)


@app.get("/")
def health_check() -> dict:
    return {}
