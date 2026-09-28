from github import Github 
import os

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
g = Github(GITHUB_TOKEN)

class Github():
    def __init__(self):
        pass

    def repo_info(self, repo_url: str) -> dict:
        """"
        Get information about a Github repository
        """
        repo = g.get_repo(repo_url)
        return {
            "name": repo.name,
            "full_name": repo.full_name,
            "description": repo.description,
            "url": repo.html_url,
            "stars": repo.stargazers_count,
            "forks": repo.forks_count,
            "open_issues": repo.open_issues_count,
            "watchers": repo.watchers_count,
            "language": repo.language,
            "created_at": repo.created_at.isoformat(),
        }
    def list_issues(self, repo_url: str, state: str = "open") -> list[dict]:
        """"
        List all the open issues in a Github repository
        """
        issues = g.get_repo(repo_url).get_issues(state=state)
        return [
            {
                "title": issue.title,
                "number": issue.number,
                "url": issue.html_url,
                "state": issue.state,
                "created_at": issue.created_at.isoformat(),
                "updated_at": issue.updated_at.isoformat(),
            }
            for issue in issues
        ]


    def list_prs(self, repo_url:str, state:str = "open") -> list[dict]:
        """
        List all the open pull requests in a github repository.
        """
        pr = g.get_repo(repo_url).get_pulls(state=state)
        return [
            {
                "title": pr.title,
                "number": pr.number,
                "url": pr.html_url,
                "state": pr.state,
                "created_at": pr.created_at.isoformat(),
                "updated_at": pr.updated_at.isoformat(),
            }
            for pr in pr
        ]


