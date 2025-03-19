from .lister_generic import GenericLister
import os
import requests


class GithubLister(GenericLister):
    """
    GithubLister fetches versions from api.github.com releases of given repo.

    repo:
    - the repo part of github url (e.g. "kubernetes-sigs/kustomize")

    url:
    - the url to query for versions
    - default: https://api.github.com/repos/{repo}/releases
    """

    def __init__(self, repo: str):
        super().__init__(f"https://api.github.com/repos/{repo}/releases")
        self.params = {"per_page": 100, "page": 1}
        token = os.environ.get("GITHUB_API_TOKEN")
        if token:
            if self.headers is None:
                self.headers = {}
            self.headers["Authorization"] = f"token {token}"

    def has_more_pages(self, response: requests.Response) -> bool:
        """Returns true if the response indicates there are more pages."""
        return 'rel="next"' in response.headers.get("Link", "")

    def do_requests(self) -> list[requests.Response]:
        """HTTP request all pages of the version page."""
        response_list = list()
        while True:
            response = requests.get(
                self.url,
                params=self.params,
                headers=self.headers,
            )
            response.raise_for_status()
            response_list.append(response)
            if not self.has_more_pages(response):
                break
            self.params["page"] += 1
        return response_list

    def extract_versions(self, response: requests.Response) -> list[str]:
        """Extracts the relevant version strings from the response."""
        data = response.json()
        versions = list()
        for item in data:
            if not item["prerelease"] and not item["draft"]:
                versions.append(item["tag_name"])
        return versions
