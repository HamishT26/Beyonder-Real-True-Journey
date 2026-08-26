"""Owner-local Typer import and command-construction smoke."""
import typer

app = typer.Typer(add_completion=False)


@app.command()
def check() -> None:
    """Emit only the bounded synthetic smoke state."""
    typer.echo("BOUNDED_SYNTHETIC_ONLY")


if __name__ == "__main__":
    app()
