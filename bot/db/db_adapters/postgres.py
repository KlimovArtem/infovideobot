import os

import asyncpg
from asyncpg import Pool
from dotenv import load_dotenv

load_dotenv()

class Postgres:
    def __init__(self, database_url: str):
        self.database_url: str = database_url

    async def connect(self):
        self.pool: Pool = await asyncpg.create_pool(self.database_url)

    async def disconnect(self):
        self.pool.terminate()

database = Postgres(os.getenv("DB_URL", ""))