import contextlib
import os
from collections.abc import Generator
from pathlib import Path
from typing import Any

from invoke import Context, task


# context manager that make sure subsequent
# commands are run in the specified directory
@contextlib.contextmanager
def cwd(rel_path: str) -> Generator[Any, Any, Any]:
    prev_cwd = Path.cwd()
    try:
        os.chdir(Path(__file__).parent / rel_path)
        yield
    finally:
        os.chdir(prev_cwd)


@task
def dev(c: Context) -> None:
    with cwd("observable"):
        c.run("yarn dev")


@task
def update_movies_dataset(c: Context) -> None:
    c.run("python -m observatoire.tmdb.movies")


@task
def clean_branches(c: Context) -> None:
    c.run("git branch --merged | grep -v '\\*\\|main' | xargs -n 1 git branch -d")
