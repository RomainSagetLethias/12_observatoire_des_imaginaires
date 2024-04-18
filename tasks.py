from invoke import Context, task


@task
def update_movies_dataset(c: Context) -> None:
    c.run("python -m observatoire.tmdb.movies")


@task
def clean_branches(c: Context) -> None:
    c.run("git branch --merged | grep -v '\\*\\|main' | xargs -n 1 git branch -d")
