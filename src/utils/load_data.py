import asyncio
import argparse
import json
import logging

from bot.db import schemes
from bot.db.db_adapters import postgres as db_adapter
from bot.db import migrate

logging.basicConfig(level=logging.DEBUG)

parser = argparse.ArgumentParser()
parser.add_argument("filepath")


async def preparing_data(data: dict):
    videos = []
    snapshots = []
    for video in data:
        logging.debug(f"Вырезаем снапшоты и передаём в pydantic.")
        snapshots.append(
            [tuple(schemes.Snapshot(**snapshot).__dict__.values())
             for snapshot in video.pop("snapshots")]
        )
        video = schemes.Video(**video)
        video_tuple = tuple(video.__dict__.values())
        videos.append(video_tuple)
    return videos, snapshots


async def insert_data(videos: list, snapshots: list):
    video_query = """
    INSERT INTO videos(
        id,
        creator_id,
        video_created_at,
        views_count,
        likes_count,
        comments_count,
        reports_count,
        created_at,
        updated_at)
    VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9);"""

    snapshot_query = """
    INSERT INTO snapshots(
        id,
        video_id
        views_count,
        likes_count,
        comments_count,
        reports_count,
        delta_views_count,
        delta_likes_count,
        delta_reports_count,
        delta_comments_count,
        created_at,
        updated_at)
    VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, %12);
    """

    if hasattr(db_adapter.database, "pool"):
        db_adapter.database.connect()

    migrate.apply_pending_migrations()

    async with db_adapter.database.pool.acquire as connection:
        connection.executemany(video_query, videos)
        connection.executemany(snapshot_query, snapshots)


async def from_json(filepath: str):
    logging.info("Загрузка данных из файла...")
    logging.debug("Загрузка данных из файла {filepath}")
    try:
        data: dict | None = None
        with open(filepath, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        logging.error(f"Ошибка загрузки данных, файл {filepath} не найден.")

    videos, snapshots = await preparing_data(data.get("videos"))
    await insert_data(videos, snapshots)

if __name__ == "__main__":
    args = parser.parse_args()
    asyncio.run(from_json(args.filepath))
