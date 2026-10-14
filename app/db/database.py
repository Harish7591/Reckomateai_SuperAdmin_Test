
import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGODB_URI = os.getenv(
    "MONGODB_URI",
    "mongodb://localhost:27017",
)

MONGODB_DB = os.getenv(
    "MONGODB_DB",
    "reckomate_sample",
)

client = MongoClient(
    MONGODB_URI,
    serverSelectionTimeoutMS=5000,
)

database = client[MONGODB_DB]


def check_mongodb_connection():
    try:
        client.admin.command("ping")
        return {
            "status": "connected",
            "database": MONGODB_DB,
        }
    except Exception as exc:
        return {
            "status": "error",
            "message": str(exc),
        }
