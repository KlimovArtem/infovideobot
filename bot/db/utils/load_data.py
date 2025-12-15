import asyncio
import argparse
import json
import logging
import os

from bot.db import schemes
from bot.db.db_adapters import postgres as db_adapter
from bot.db import migrate


load_dotenv()

logging.basicConfig(level=logging.DEBUG)

parser = argparse.ArgumentParser(
    prog='load_data',
    description='Load data to database',
    epilog=''
)

parser.add_argument('-t', '--type')
parser.add_argument('filepath')

path = "/Users/ekaterinaklimova/Documents/Разработка/infovideobot/data/videos.json"

async def transform_data_types(data: dict):
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
        updated_at
    ) VALUES(
        $1,
        $2,
        $3,
        $4,
        $5,
        $6,
        $7,
        $8,
        $9
    );"""
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
        updated_at
    ) VALUES(
        $1,
        $2,
        $3,
        $4,
        $5,
        $6,
        $7,
        $8,
        $9,
        $10,
        $11,
        %12
    );"""
    await db_adapter.database.content()
    
    async with db_adapter.database.pool as connection:
        await connection.executemany(video_query, videos)
        await connection.executemany(snapshot_query, snapshots)
        res = await connection.fetch("SELECT * FROM videos;")
        logging.debug(f"{res[0]}")
    await db_adapter.database.content()
        


async def from_json(filepath: str):
    logging.info("Загрузка данных из файла...")
    logging.debug("Загрузка данных из файла {filepath}")
    try:
        data: dict | None = None
        with open(filepath, "r") as file:
            data = json.load(file)
    except FileNotFoundError as e:
        logging.error(f"Ошибка загрузки данных, файл {filepath} не найден.")

    videos, snapshots = await transform_data_types(data.get("videos"))
    await insert_data(videos, snapshots)

if __name__ == "__main__":
    args = parser.parse_args()
    if args.type == "json" or None:
        asyncio.run(from_json(args.filepath))