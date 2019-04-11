import click

from . import fetch
from .api import create_api
from .store import store


@click.command()
@click.argument("filename", type=click.Path(exists=True, dir_okay=False))
@click.argument("dest", type=click.Path(dir_okay=False))
@click.option("--limit", "-l", type=int)
@click.option("--count", "-c", type=int, default=50)
def main(filename, dest: str, limit: int, count: int):
    api = create_api()

    click.echo("Operation plan:")
    click.echo(
        f"1. Load {limit or 'all'} users from '{filename}'.\n"
        f"2. Fetch {count} tweets from each user.\n"
        f"3. Store them in file '{dest}'.\n"
    )
    if not click.confirm("Does this sound okay?"):
        raise click.Abort

    click.echo("Hang tight, this may take some time…")

    tweets = fetch.from_csv(filename, limit=limit, count=count, api=api)
    store(tweets, dest)


if __name__ == "__main__":
    main()
