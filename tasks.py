from invoke import Context, task


@task
def clean_branches(c: Context) -> None:
    c.run("git branch --merged | grep -v '\\*\\|main' | xargs -n 1 git branch -d")
