import requests
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("GITHUB_TOKEN")

headers = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github+json"
}


def get_repos():
    url = "https://api.github.com/user/repos"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return []

    repos = response.json()

    return [repo["name"] for repo in repos]


def get_default_branch(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return "main"  # fallback

    data = response.json()
    return data.get("default_branch", "main")


def trigger_workflow(owner, repo):
    # 🔥 get correct branch automatically
    branch = get_default_branch(owner, repo)

    url = f"https://api.github.com/repos/{owner}/{repo}/actions/workflows/auto-patch.yml/dispatches"

    data = {
        "ref": branch
    }

    try:
        response = requests.post(url, headers=headers, json=data)

        return {
            "status_code": response.status_code,
            "branch_used": branch
        }

    except Exception as e:
        return {
            "status_code": 500,
            "error": str(e)
        }