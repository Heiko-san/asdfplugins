from .downloader_generic import GenericDownloader
import os


class GithubDownloader(GenericDownloader):
    """
    GithubDownloader

    repo:
    - the repo part of github url (e.g. "kubernetes-sigs/kustomize")

    url:
    - same rules apply as for GenericDownloader's url
    - defaults to "https://github.com/{repo}/releases/download/v{version}"
    """

    def __init__(
        self,
        repo: str,
        url: str = "https://github.com/{repo}/releases/download/v{version}",
    ):
        self.repo = repo
        super().__init__(url)
        token = os.environ.get("GITHUB_API_TOKEN")
        if token:
            if self.headers is None:
                self.headers = {}
            self.headers["Authorization"] = f"token {token}"

    def template(self, string: str, **kwargs) -> str:
        """Render a string with repo, platform, arch, version & kwargs."""
        return super().template(string, repo=self.repo, **kwargs)
