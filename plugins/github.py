

class Github():
    def __init__(self):
        pass

    def repo_info(self, repo_url: str) -> dict:
        """"
        Get information about a Github repository
        """
        pass

    def list_issues(self, repo_url: str, state: str = "open") -> list[dict]:
        """"
        List all the open issues in a Github repository
        """
        pass

    def list_prs(self, repo_url:str, state:str = "open") -> list[dict]:
        """
        List all the open pull requests in a github repository.
        """
        pass


