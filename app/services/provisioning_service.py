
from app.db.organisation_repository import (
    update_organisation_status,
)
from app.services.github_service import create_organisation_branch


def provision_organisation(slug: str):
    try:
        update_organisation_status(slug, "PROVISIONING")

        branch_result = create_organisation_branch(slug)

        update_organisation_status(
            slug,
            "BRANCH_CREATED",
        )

        print(
            f"GitHub branch ready: "
            f"{branch_result['repository']}/tree/"
            f"{branch_result['branch_name']}"
        )

    except Exception as exc:
        update_organisation_status(
            slug,
            "FAILED",
            error=str(exc),
        )
        print(f"Provisioning failed for {slug}: {exc}")
