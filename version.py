__all__ = "get_git_version"

from subprocess import PIPE, Popen


def get_git_tag() -> str:
    p = Popen(
        ["git", "describe", "--tags"],
        stdout=PIPE,
        stderr=PIPE,
    )
    assert p.stderr is not None
    assert p.stdout is not None
    p.stderr.close()
    lines = p.stdout.readlines()
    return lines[0].strip().decode()
