from fastapi import FastAPI
from .api import tokens
from .database.config import engine, Base

app = FastAPI(title="Push Notification Token Service")

@app.on_event("startup")
async def startup():
    # Create database tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("shutdown")
async def shutdown():
    # Close database connections
    await engine.dispose()

app.include_router(tokens.router, prefix="/api/v1", tags=["tokens"])