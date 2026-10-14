
import os
from dotenv import load_dotenv
from github import Github, GithubException

load_dotenv()

token = os.getenv("GITHUB_TOKEN")
owner = os.getenv("GITHUB_OWNER")
repo_name = os.getenv("ORG_TEMPLATE_REPO")

if not token or not owner or not repo_name:
    print("ERROR: Check GITHUB_TOKEN, GITHUB_OWNER, and ORG_TEMPLATE_REPO in .env")
    raise SystemExit(1)

try:
    gh = Github(token)
    repository = gh.get_repo(f"{owner}/{repo_name}")

    print("GitHub connection: SUCCESS")
    print("Repository:", repository.full_name)
    print("Default branch:", repository.default_branch)
    print("Available branches:")

    for branch in repository.get_branches():
        print("-", branch.name)

except GithubException as e:
    print("GitHub API error:", e.status)
    print(e.data.get("message", str(e)))
