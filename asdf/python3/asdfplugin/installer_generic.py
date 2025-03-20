from .base_generic_install import GenericInstallBase
import os
import re
import stat
import gzip
import tarfile
import zipfile
import shutil
import pathlib
from typing import Self


def is_gzip_file(filepath):
    """Returns true if given file is gzip encoded."""
    with open(filepath, "rb") as test_f:
        return test_f.read(2) == b"\x1f\x8b"


class GenericInstaller(GenericInstallBase):
    """
    GenericInstaller extracts downloaded file and installs the executables
    from it.
    """

    def __init__(self):
        super().__init__()

    def install(
        self,
        files: dict[str, str | re.Pattern | None],
        source: str = "",
    ) -> Self:
        r"""
        Implements asdf's install functionality.

        files:
        - key is the name of executable to install
            - install this executable into ${ASDF_INSTALL_PATH}/bin/
            - can be an actualy file name
                (e.g. "mybin")
            - can be a pattern to template
                (e.g. "mybin.{platform}-{arch}.{version}"),
                if value is not a re.Pattern
            - can be replacement pattern for re.sub()
                (see e.g. jsonnet), if value is a re.Pattern
        - value is its source
            - choose this as the source file from ${ASDF_DOWNLOAD_PATH}
            - can be an actualy file name
                (e.g. "path/to/mybin")
            - can be a pattern to template
                (see e.g. helm, krew)
            - can be a re.Pattern to match files in ${ASDF_DOWNLOAD_PATH}
                (see e.g. jsonnet)
            - can be None to try to find a file named as key
                or fall back to source file

        source:
        - this refers to the downloaded file / archive
        - can be a pattern to template (e.g. "downloaded.{platform}-{arch}")
        - defaults to self.default_local_file from GenericInstallBase

        Returns self to allow chaining.
        """
        if not source:
            source = self.default_local_file
        source = self.template(source)
        source_path = os.path.join(self.download_path, source)
        assert os.path.isfile(source_path), f"{source_path} doesn't exist"
        if is_gzip_file(source_path):
            source = self.gunzip(source)
        source_path = os.path.join(self.download_path, source)
        if zipfile.is_zipfile(source_path):
            self.unzip(source)
        if tarfile.is_tarfile(source_path):
            self.untar(source)
        self.install_files(files, source)
        return self

    def gunzip(self, source: str) -> str:
        """Unzip a gzip archive."""
        target = source + ".unzipped"
        target_path = os.path.join(self.download_path, target)
        source_path = os.path.join(self.download_path, source)
        print(f"unzipping {source_path} to {target_path}")
        with gzip.open(source_path, "rb") as f_in:
            with open(target_path, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)
        return target

    def unzip(self, source: str):
        """Unzip a zip archive."""
        target_path = self.download_path
        source_path = os.path.join(self.download_path, source)
        print(f"unzipping {source_path} to {target_path}/")
        zipfile.ZipFile(source_path).extractall(target_path)

    def untar(self, source: str):
        """Untar a tarball."""
        target_path = self.download_path
        source_path = os.path.join(self.download_path, source)
        print(f"untaring {source_path} to {target_path}/")
        with tarfile.open(source_path) as f:
            f.extractall(path=target_path)

    def install_files(
        self,
        files: dict[str, str | re.Pattern | None],
        source_file: str,
    ):
        """Install executable files from download to install directory."""
        for target, source in files.items():
            if isinstance(source, re.Pattern):
                dl_files_path = pathlib.Path(self.download_path)
                dl_files = [
                    str(item.relative_to(dl_files_path))
                    for item in dl_files_path.rglob("*")
                    if item.is_file()
                ]
                for dl_file in dl_files:
                    if source.search(dl_file):
                        target_name = source.sub(target, dl_file)
                        self.install_file(dl_file, target_name)
            else:
                if source is None:
                    source = source_file
                    if os.path.isfile(os.path.join(self.download_path, target)):
                        source = target
                self.install_file(self.template(source), self.template(target))

    def install_file(self, source: str, target: str):
        """Install a single executable from download to install directory."""
        source_path = os.path.join(self.download_path, source)
        target_path = os.path.join(self.install_path, "bin", target)
        print(f"installing {source_path} to {target_path}")
        dir_path = os.path.dirname(target_path)
        if not os.path.isdir(dir_path):
            os.mkdir(dir_path)
        os.rename(source_path, target_path)
        st = os.stat(target_path)
        x_bits = stat.S_IXGRP | stat.S_IXUSR | stat.S_IXOTH
        os.chmod(target_path, st.st_mode | x_bits)
