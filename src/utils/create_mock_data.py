from datetime import datetime
import json
import random
import uuid



    
    
def main():
    data = {}
    data["videos"] = [
        {
            "id": str(uuid.uuid4()),
            "creator_id": str(uuid.uuid4()),
            "video_created_at": str(datetime(2025, random.randint(1, 12), random.randint(1, 25), random.randint(0, 23), random.randint(0, 59))),
            "views_count": random.randint(0, 1000),
            "likes_count": random.randint(0, 500),
            "comments_count": random.randint(0, 500),
            "reports_count": random.randint(0, 200),
            "created_at": str(datetime(2025, random.randint(1, 12), random.randint(1, 25), random.randint(0, 23), random.randint(0, 59))),
            "updated_at": str(datetime(2025, random.randint(1, 12), random.randint(1, 25), random.randint(0, 23), random.randint(0, 59)))
        } 
        for _  in range(10)
    ]

    for video in data["videos"]:
        video["snapshots"] = [
            {
                "id": str(uuid.uuid4()),
                "video_id": video.get("id"),
                "views_count": random.randint(0, 1000),
                "likes_count": random.randint(0, 500),
                "comments_count": random.randint(0, 500),
                "reports_count": random.randint(0, 200),
                "delta_views_count": random.randint(0, 100),
                "delta_likes_count": random.randint(0, 50),
                "delta_comments_count": random.randint(0, 50),
                "delta_reports_count": random.randint(0, 20),
                "created_at": str(datetime(2025, random.randint(1, 12), random.randint(1, 25), random.randint(0, 23), random.randint(0, 59))),
                "updated_at": str(datetime(2025, random.randint(1, 12), random.randint(1, 25), random.randint(0, 23), random.randint(0, 59)))
            }
            for _ in range(5)
        ]

    with open("data.json", "w") as file:
        json.dump(data, file)


if __name__ == "__main__":
    main()
