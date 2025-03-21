import re
from packaging.version import Version
from typing import TextIO


class VersionConstraint(object):
    """
    VersionConstraint implements a class to interpret terraform like version
    constraints.
    """

    def __init__(self, constraints: list[tuple[str, str]]):
        self._original = constraints
        self.constraints = list()
        for operator, semver_str in constraints:
            version = Version(semver_str)
            if operator == "=":
                self.constraints.append(version.__eq__)
            elif operator == "!=":
                self.constraints.append(version.__ne__)
            elif operator == ">":
                self.constraints.append(version.__lt__)
            elif operator == "<":
                self.constraints.append(version.__gt__)
            elif operator == ">=":
                self.constraints.append(version.__le__)
            elif operator == "<=":
                self.constraints.append(version.__ge__)
            elif operator == "~>":
                # ~> 1.10.5 is the same as
                # >= 1.10.5, < 1.11.0
                self.constraints.append(version.__le__)
                self.constraints.append(
                    Version(f"{version.major}.{version.minor+1}.0").__gt__,
                )
            else:
                raise ValueError(f'operator "{operator}" not supported')

    def __str__(self) -> str:
        return ", ".join([" ".join(tpl) for tpl in self._original])

    def test_version(self, version: str) -> bool:
        """Returns true if given version meets all constraints."""
        version_obj = Version(version)
        return all([test(version_obj) for test in self.constraints])

    def filter_versions(self, versions: list[str]) -> list[str]:
        """Filters the given list by all constraints."""
        return [v for v in versions if self.test_version(v)]

    def latest_matching(self, versions: list[str]) -> str | None:
        """
        Returns the latest matching version from given list.
        Returns None if no version matches the constraints.
        """
        filtered_versions = self.filter_versions(versions)
        if not filtered_versions:
            return None
        filtered_versions.sort(key=Version)
        return filtered_versions[-1]


def constraint_from_tf_string(constraint: str) -> VersionConstraint:
    """
    Create a VersionConstraint from a constraint string as used inside terraform
    versioning block (e.g. ">= 1.10.5, < 1.12", "~> 1.10.5" or "1.10.5").
    """
    constraints = list()
    for item in constraint.split(","):
        tokens = item.strip().split(" ")
        if len(tokens) == 1:
            constraints.append(("=", tokens[0].strip()))
        else:
            constraints.append((tokens[0].strip(), tokens[1].strip()))
    return VersionConstraint(constraints)


terraform_block_start = re.compile(r"^terraform\s+{\s*$")
block_end = re.compile(r"^}/s*$")
constraint_re = r"\s*[!=<>~]{0,2}\s*(?:[0-9]+\.){0,2}[0-9]+\s*"
constraints_re = r"((?:" + constraint_re + r",)*" + constraint_re + r")"
terraform_version = re.compile(
    r'^\s*required_version\s*=\s*"' + constraints_re + r'"\s*$'
)


def constraint_from_tf_file(file: TextIO) -> VersionConstraint | None:
    """
    Create a VersionConstraint from a .tf file which contains a
    "required_version" constraint line inside a terraform block.
    Returns None, if no such line can be found.
    """
    in_terraform_block = False
    for line in file.readlines():
        if terraform_block_start.match(line):
            in_terraform_block = True
        elif in_terraform_block:
            if block_end.match(line):
                in_terraform_block = False
            else:
                match = terraform_version.match(line)
                if match:
                    return constraint_from_tf_string(match.group(1))
    return None
