from .base_generic_install import GenericInstallBase
import os
import requests
from typing import Self


class GenericDownloader(GenericInstallBase):
    """
    GenericDownloader downloads files from a given url.

    url:
    - the base url to append files to download
    - "{filename}" will be replaced with the files to download
    - if url doesn't contain "{filename}" then "/{filename}" will be added to it
    """

    def __init__(self, url: str):
        super().__init__()
        self.url = url
        if "{filename}" not in self.url:
            self.url += "/{filename}"
        self.headers = None
        self.params = None

    def download(self, file: str, target: str = "") -> Self:
        """
        Implements asdf's download functionality.

        file:
        - the file to download from GenericDownloader's url
        - can be a pattern to template (e.g. "foo-{platform}-{arch}.{version}")

        target:
        - the target file name to store the downloaded file to
        - can be a pattern to template (e.g. "downloaded.{platform}-{arch}")
        - defaults to self.default_local_file from GenericInstallBase

        Returns self to allow chaining.
        """
        if not target:
            target = self.default_local_file
        target = self.template(target)
        url = self.get_download_url(file)
        target_path = os.path.join(self.download_path, target)
        print(f"downloading {url} to {target_path}")
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(target_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return self

    def get_download_url(self, file: str) -> str:
        """Render the URL to download the given file from."""
        return self.template(self.url, filename=self.template(file))
