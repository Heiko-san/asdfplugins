from .base_generic_list import GenericListBase
import requests


class GenericLister(GenericListBase):
    """
    GenericLister fetches versions from an url by applying the filter regex
    to the page.

    url:
    - the url to query for versions
    """

    def __init__(self, url: str):
        self.url = url
        self.headers = None
        self.params = None

    def do_requests(self) -> list[requests.Response]:
        """HTTP request the version page."""
        response = requests.get(self.url, params=self.params, headers=self.headers)
        response.raise_for_status()
        return [response]

    def extract_versions(self, response: requests.Response) -> list[str]:
        """Extracts the relevant version strings from the response."""
        return self.version_filter.findall(str(response.content))

    def get_versions(self) -> list[str]:
        """Retrieves a list of all versions..."""
        versions = list()
        for response in self.do_requests():
            versions.extend(self.extract_versions(response))
        return versions
