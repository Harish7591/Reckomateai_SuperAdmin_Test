
from datetime import datetime, timezone

from pymongo.errors import DuplicateKeyError

from app.db.database import database
from app.models.organisation import organisation_document

organisations_collection = database["organisations"]
organisations_collection.create_index("slug", unique=True)


def create_organisation(name: str, slug: str) -> dict:
    document = organisation_document(name, slug)
    document["created_at"] = datetime.now(timezone.utc)

    result = organisations_collection.insert_one(document)
    document["_id"] = result.inserted_id
    return document


def get_organisation_by_slug(slug: str):
    return organisations_collection.find_one({"slug": slug})


def list_organisations():
    return list(
        organisations_collection.find(
            {},
            {"name": 1, "slug": 1, "branch_name": 1, "status": 1},
        )
    )

def update_organisation_status(slug: str, status: str, error: str = None):
    organisations_collection.update_one(
        {"slug": slug},
        {
            "$set": {
                "status": status,
                "error": error,
                "updated_at": datetime.now(timezone.utc),
            }
        },
    )