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
    Only get_versions() needs to be implemented in actual subclasses
    deduplication, sorting and output is already implemented here.
    The modify(kwargs) function can be used to override attributes in a
    chainable way.
    """

    def list_all(
        self,
        filter: str = r"^v?((?:[0-9]+\.){2}[0-9]+)$",
    ) -> Self:
        r"""
        Implements asdf's list-all functionality.

        filter:
        - filter needs to have exactly 1 catching group
        - only versions matching the filter will be considered
        - only the part matching the catching group will be used as the version
        - default semver (stable): r"^v?((?:[0-9]+\.){2}[0-9]+)$"

        Returns self to allow chaining.
        """
        print(" ".join(self.get_final_versions(filter)))
        return self

    def get_final_versions(self, filter: str) -> list[str]:
        """Returns the final, deduplicated and sorted versions list."""
        self.version_filter = re.compile(filter)
        return self.sort_versions(list(set(self.get_versions())))

    def get_versions(self) -> list[str]:
        """
        Retrieves a list of all versions, before modify and sort gets applied.
        Override this in actual implementation.
        """
        return []

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
