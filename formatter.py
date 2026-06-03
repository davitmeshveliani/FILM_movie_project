from typing import List, Any
from rich.console import Console
from rich.table import Table

console = Console()


def display_movies(movies: List[Any]) -> None:
    """
    Displays a list of movies in a formatted table.

    Args:
        movies (List[Any]): A list of movie objects (namedtuples) to display.
    """
    table = Table(show_header=True, header_style="bold magenta", border_style="blue")
    table.add_column("#", style="dim", width=4)
    table.add_column("Movie Title", style="bold cyan")
    table.add_column("Year", justify="center")
    table.add_column("Rating", justify="center")
    table.add_column("Length", justify="right")

    for idx, movie in enumerate(movies, 1):
        table.add_row(
                    str(idx),
                    movie.title,
                    str(movie.release_year),
                    movie.rating,
                    f"{movie.length} min."
                    )
    console.print(table)


def display_stats(stats: List[Any]) -> None:
    """
    Displays the top 5 most popular searches in a formatted table.

    Args:
        stats (List[Any]): A list of search statistics objects to display
    """
    table = Table(
                title="[bold yellow]TOP 5 MOST POPULAR SEARCHES[/]",
                show_header=True,
                header_style="bold magenta",
                border_style="blue"
                )
    table.add_column("#", style="dim", width=4)
    table.add_column("Query", style="bold cyan")
    table.add_column("Count", justify="right", style="bold green")

    if not stats:
        console.print("[bold red]No search history recorded yet.[/]")
    else:
        for idx, stat in enumerate(stats, 1):
            table.add_row(str(idx), stat.keyword, str(stat.count))

    console.print(table)