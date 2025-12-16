from config.config import async_session


async def get_db():
    # db = SessionLocal()
    # try:
    #     yield db
    # finally:
    #     db.close()
    async with async_session() as session:
        yield session