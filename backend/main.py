from fastapi import FastAPI
from github import get_repos, trigger_workflow
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")

@app.get("/")
def home():
    return {"message": "Backend is working"}

@app.get("/repos")
def repos():
    return {"repos": get_repos()}

@app.post("/trigger/{repo_name}")
def trigger(repo_name: str):
    result = trigger_workflow(GITHUB_USERNAME, repo_name)

    return {
        "repo": repo_name,
        "status": result["status_code"],
        "note": interpret_status(result["status_code"])
    }

@app.post("/trigger-all")
def trigger_all():
    repos = get_repos()

    results = []
    success = 0
    failed = 0

    for repo in repos:
        res = trigger_workflow(GITHUB_USERNAME, repo)
        status = res["status_code"]

        if status == 204:
            success += 1
        else:
            failed += 1

        results.append({
            "repo": repo,
            "status": status,
            "note": interpret_status(status)
        })

    return {
        "total_repos": len(repos),
        "success": success,
        "failed": failed,
        "results": results
    }


def interpret_status(status_code):
    if status_code == 204:
        return "Workflow triggered successfully"
    elif status_code == 404:
        return "Workflow file not found in repo"
    elif status_code == 401:
        return "Unauthorized (check token)"
    elif status_code == 422:
        return "Invalid request (check branch name)"
    else:
        return "Unknown response"