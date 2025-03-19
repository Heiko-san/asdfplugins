import os
import re
import platform
from typing import Self


class GenericInstallBase(object):
    """
    GenericInstallBase provides the basic framework for install & download
    commands.
    Provides get_arch() function to map platform type, template(string) to
    render those informations into strings & modify(kwargs) to override
    attributes like arch mappings.
    """

    def __init__(self):
        self._init_env()
        self._init_arch()
        # uname_result(system='Linux', machine='x86_64', ...)
        # uname_result(system='Windows', machine='AMD64', ...)
        self.uname = platform.uname()
        self.default_local_file = "downloaded.file"

    def _init_env(self):
        """Check and load ASDF_* environment variables."""
        # ASDF_DOWNLOAD_PATH = /home/user/.asdf/downloads/sops/3.9.4
        self.download_path = os.environ.get("ASDF_DOWNLOAD_PATH")
        assert self.download_path is not None, "ASDF_DOWNLOAD_PATH missing"
        # ASDF_INSTALL_PATH = /home/user/.asdf/installs/sops/3.9.4
        self.install_path = os.environ.get("ASDF_INSTALL_PATH")
        assert self.install_path is not None, "ASDF_INSTALL_PATH missing"
        # ASDF_INSTALL_VERSION = 3.9.4
        self.install_version = os.environ.get("ASDF_INSTALL_VERSION")
        assert self.install_version is not None, "ASDF_INSTALL_VERSION missing"
        # ASDF_INSTALL_TYPE = version | ref
        self.install_type = os.environ.get("ASDF_INSTALL_TYPE")
        assert (
            self.install_type == "version"
        ), 'only ASDF_INSTALL_TYPE "version" supported'

    def _init_arch(self):
        """Initialize all the platform/arch overrides."""
        self.platform_lower = True
        self.arch_amd64_re = re.compile(r"^(amd|x86_)64$")
        self.arch_amd64_value = "amd64"
        self.arch_arm64_re = re.compile(r"^(arm64|aarch64|armv8l)$")
        self.arch_arm64_value = "arm64"
        self.arch_s390_re = re.compile(r"^s390x?$")
        self.arch_s390_value = "s390x"
        self.arch_ppc64_re = re.compile(r"^ppc64le$")
        self.arch_ppc64_value = "ppc64le"
        self.arch_386_re = re.compile(r"^i\d86$")
        self.arch_386_value = "386"

    def get_arch(self) -> tuple[str, str]:
        """
        Returns (platform, arch) strings for this system, based on the global
        arch mapping settings.
        """
        pf = self.uname.system
        if self.platform_lower:
            pf = pf.lower()
        arch = self.uname.machine.lower()
        if self.arch_386_re.search(arch):
            arch = self.arch_386_value
        elif self.arch_ppc64_re.search(arch):
            arch = self.arch_ppc64_value
        elif self.arch_arm64_re.search(arch):
            arch = self.arch_arm64_value
        elif self.arch_s390_re.search(arch):
            arch = self.arch_s390_value
        else:
            arch = self.arch_amd64_value
        return pf, arch

    def template(self, string: str, **kwargs: dict[str, any]) -> str:
        """Render a string with platform, arch, version & kwargs."""
        pf, arch = self.get_arch()
        return string.format(
            arch=arch,
            platform=pf,
            version=self.install_version,
            **kwargs,
        )

    def modify(self, **kwargs: dict[str, any]) -> Self:
        """
        Modify multiple attributes of this object.
        Returns self to allow chaining.
        """
        for k, v in kwargs.items():
            self.__setattr__(k, v)
        return self
