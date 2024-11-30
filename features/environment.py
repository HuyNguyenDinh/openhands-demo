import os
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from app.database.config import Base

# Test database URL
TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/push_notifications_test"

def before_all(context):
    """Set up the test environment before all tests."""
    # Set test database URL
    os.environ["DATABASE_URL"] = TEST_DATABASE_URL
    
    # Create test engine
    context.engine = create_async_engine(TEST_DATABASE_URL)
    
    # Create event loop
    context.loop = asyncio.new_event_loop()
    asyncio.set_event_loop(context.loop)

def before_scenario(context, scenario):
    """Set up the database before each scenario."""
    async def setup_db():
        async with context.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
    
    context.loop.run_until_complete(setup_db())

def after_scenario(context, scenario):
    """Clean up after each scenario."""
    async def cleanup_db():
        async with context.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
    
    context.loop.run_until_complete(cleanup_db())

def after_all(context):
    """Clean up after all tests."""
    async def dispose_engine():
        await context.engine.dispose()
    
    context.loop.run_until_complete(dispose_engine())
    context.loop.close()