
from datetime import datetime, timezone


def organisation_document(
    name: str,
    slug: str,
) -> dict:
    now = datetime.now(timezone.utc)

    return {
        "name": name,
        "slug": slug,
        "branch_name": f"org_{slug.replace('-', '_')}",
        "status": "PENDING",
        "container_name": f"org_{slug.replace('-', '_')}_backend",
        "created_at": now,
        "updated_at": now,
        "error": None,
    }
