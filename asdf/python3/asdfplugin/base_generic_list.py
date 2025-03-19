import re
from packaging.version import Version
from typing import Self


def sort_alphanumeric(versions: list[str]) -> list[str]:
    """Sort versions alphabetically."""
    versions.sort()
    return versions


def sort_versions(versions: list[str]) -> list[str]:
    """Sort versions by its major, minor & patch version."""
    versions.sort(key=Version)
    return versions


class GenericListBase(object):
    """
    GenericListBase provides the basic implementation of list_all().
    Only get_raw_versions() needs to be implemented in actual subclasses.
    The modify(kwargs) function can be used to override attributes in a
    chainable way.
    """

    def list_all(
        self,
        filter: str = r"^v?(?:[0-9]+\.){2}[0-9]+$",
        replace: str = r"^v",
        replacement: str = "",
    ) -> Self:
        r"""
        Implements asdf's list-all functionality.

        filter:
        - all versions returned by get_raw_versions() first will be matched
            against this pattern by re.search(filter)
        - only those versions that match will be kept
        - default semver (stable): r"^v?(?:[0-9]+\.){2}[0-9]+$"

        replace:
        - the filtered versions will be modified by re.sub(replace, replacement)
        - find all occurrences of this pattern and replace them with replacement
        - default remove leading "v": r"^v"

        replacement:
        - replace all findings of the replace parameter by this string
        - default remove: ""

        Returns self to allow chaining.
        """
        self.version_filter = re.compile(filter)
        self.version_replace = re.compile(replace)
        self.version_replacement = replacement
        versions = self.modify_versions(self.get_raw_versions())
        print(" ".join(self.sort_versions(versions)))
        return self

    def get_raw_versions(self) -> list[str]:
        """
        Retrieves a list of all versions, before modify and sort gets applied.
        Override this in actual implementation.
        """
        return []

    def modify_versions(self, versions: list[str]) -> list[str]:
        """Applies the patterns of list_all() to the versions list."""
        new_versions = list()
        for version in versions:
            if self.version_filter.search(version):
                new_versions.append(
                    self.version_replace.sub(self.version_replacement, version)
                )
        return new_versions

    def sort_versions(self, versions: list[str]) -> list[str]:
        """Sort versions for output."""
        return sort_versions(versions)

    def modify(self, **kwargs: dict[str, any]) -> Self:
        """
        Modify multiple attributes of this object.
        Returns self to allow chaining.
        """
        for k, v in kwargs.items():
            self.__setattr__(k, v)
        return self
