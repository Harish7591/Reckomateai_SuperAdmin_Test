
import os

from dotenv import load_dotenv
from github import Auth, Github
from github.GithubException import GithubException

load_dotenv()


def get_github_repository():
    token = os.getenv("GITHUB_TOKEN")
    owner = os.getenv("GITHUB_OWNER")
    repo_name = os.getenv("ORG_TEMPLATE_REPO")

    if not token or not owner or not repo_name:
        raise ValueError(
            "GITHUB_TOKEN, GITHUB_OWNER and ORG_TEMPLATE_REPO "
            "must be configured in .env"
        )

    github = Github(auth=Auth.Token(token))
    repository = github.get_repo(f"{owner}/{repo_name}")

    return github, repository


def create_organisation_branch(slug: str) -> dict:
    branch_name = f"org_{slug.replace('-', '_')}"

    try:
        github, repository = get_github_repository()

        # Check the source branch exists.
        main_branch = repository.get_branch("main")

        # Avoid creating a duplicate branch.
        try:
            existing_branch = repository.get_branch(branch_name)
            return {
                "status": "already_exists",
                "branch_name": existing_branch.name,
                "repository": repository.full_name,
            }
        except GithubException as exc:
            if exc.status != 404:
                raise

        # Create the organisation branch from main's current commit.
        repository.create_git_ref(
            ref=f"refs/heads/{branch_name}",
            sha=main_branch.commit.sha,
        )

        return {
            "status": "created",
            "branch_name": branch_name,
            "repository": repository.full_name,
        }

    except GithubException as exc:
        raise RuntimeError(
            f"GitHub API error ({exc.status}): {exc.data}"
        ) from exc
