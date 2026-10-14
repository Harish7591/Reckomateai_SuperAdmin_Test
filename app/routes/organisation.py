
from fastapi import APIRouter, HTTPException, status
from pymongo.errors import DuplicateKeyError, PyMongoError
from app.services.github_service import create_organisation_branch
from fastapi import APIRouter, BackgroundTasks, HTTPException, status
from app.services.provisioning_service import provision_organisation

from app.db.organisation_repository import (
    create_organisation,
    get_organisation_by_slug,
    list_organisations,
)
from app.schemas.organisation import OrganisationCreate

router = APIRouter(
    prefix="/api/organisations",
    tags=["Organisations"],
)


def serialize_organisation(document: dict) -> dict:
    return {
        "id": str(document["_id"]),
        "name": document["name"],
        "slug": document["slug"],
        "branch_name": document["branch_name"],
        "status": document["status"],
    }



@router.post("", status_code=status.HTTP_201_CREATED)
def create_organisation_endpoint(
    payload: OrganisationCreate,
    background_tasks: BackgroundTasks,
):
    try:
        if get_organisation_by_slug(payload.slug):
            raise HTTPException(
                status_code=409,
                detail="Organisation slug already exists",
            )

        document = create_organisation(payload.name, payload.slug)

        background_tasks.add_task(
            provision_organisation,
            payload.slug,
        )

        return {
            **serialize_organisation(document),
            "message": "Organisation created. Automatic provisioning started.",
        }

    except HTTPException:
        raise
    except DuplicateKeyError:
        raise HTTPException(
            status_code=409,
            detail="Organisation slug already exists",
        )
    except PyMongoError:
        raise HTTPException(
            status_code=503,
            detail="Database operation failed",
        )


@router.post("/{slug}/branch")
def create_organisation_branch_endpoint(slug: str):
    organisation = get_organisation_by_slug(slug)

    if not organisation:
        raise HTTPException(
            status_code=404,
            detail="Organisation not found",
        )

    try:
        result = create_organisation_branch(slug)
        return {
            "organisation": organisation["name"],
            "slug": slug,
            "github_repository": result["repository"],
            "branch_name": result["branch_name"],
            "branch_status": result["status"],
        }
    except ValueError as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc))
    
