from decorators import InvalidYearError
from typing import List, Tuple, Any
from db_manager import MovieDatabase
from log_writer import MongoLogger
import formatter as fmt
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


def display_menu() -> str:
    """
    Displays the main navigation menu using the Rich library.
    Returns:
        str: User's menu choice.
    """
    menu_text = (
                "1. Search by Title\n"
                "2. Search by Genre & Year\n"
                "3. View Popular Searches\n"
                "4. Exit"
                 )
    console.print(Panel(menu_text, title="[bold blue]SAKILA MOVIE SEARCH SYSTEM[/]", expand=False))
    return console.input("\n[bold cyan]Selection:[/bold cyan] ").strip()


def get_valid_genre(genres: List[str]) -> str:
    """
    Prompts user to select a genre by name or index with validation.
    Args:
        genres: A list of available genre strings.
    Returns:
        str: The selected genre name.
    """
    genres_lower = [g.lower() for g in genres]

    while True:
        choice = console.input("\n[bold cyan]Genre Name or Number:[/bold cyan] ").strip().lower()
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(genres):
                return genres[idx]
        if choice in genres_lower:
            return genres[genres_lower.index(choice)]
        console.print(f"[bold red]Invalid input. Please choose 1-{len(genres)} "
                        f"or type the full name.[/bold red]")


def get_valid_year_range(min_y: int, max_y: int) -> Tuple[int, int]:
    """
    Validates user input for a range of years, raising custom errors for business logic.
    Args:
        min_y: The minimum allowed year.
        max_y: The maximum allowed year.
    Returns:
        Tuple[int, int]: The validated start and end year.
    """
    while True:
        try:
            start = console.input(f"[bold cyan]Start Year (min {min_y}):[/bold cyan] ").strip()
            end = console.input(f"[bold cyan]End Year (max {max_y}):[/bold cyan] ").strip()

            y_from = int(start) if start else min_y
            y_to = int(end) if end else max_y

            if not (min_y <= y_from <= max_y and min_y <= y_to <= max_y):
                raise InvalidYearError(f"Years must be between {min_y} and {max_y}.")

            if y_from > y_to:
                raise InvalidYearError("Start year cannot be greater than end year.")
            return y_from, y_to

        except ValueError:
            console.print("[bold red]Error: Invalid input! Please enter valid numbers.[/bold red]")
        except InvalidYearError as e:
            console.print(f"[bold red]Business Logic Error: {e}[/bold red]")


def handle_genre_search(db: MovieDatabase,logger: MongoLogger,
                                    min_y: int,max_y: int) -> None:

    """
    Orchestrates the user flow for searching movies by genre and year.
    """
    genres = db.get_genres()
    display_genres(genres)

    genre = get_valid_genre(genres)
    y_from, y_to = get_valid_year_range(min_y, max_y)

    offset = 0
    while True:
        results = db.search_by_genre_year(
                genre,y_from,y_to,offset)
        if not results:
            console.print("\n[bold yellow]No results found for your criteria.[/bold yellow]")
            break
        fmt.display_movies(results)
        if offset == 0:
            logger.save_search_log("genre_year",{
                                                "genre": genre,
                                                "from": y_from,
                                                "to": y_to
                                                 },
                                               len(results)
                                                )
        next_results = db.search_by_genre_year(genre,y_from,y_to,offset + 10)
        if not next_results:
            console.print("\n[bold yellow]--- No more search results found. ---[/bold yellow]")
            break
        if console.input("\n[bold yellow]Load next 10 results? (y/n): [/bold yellow]").lower() != "y":
            break



def handle_keyword_search(db: MovieDatabase, logger_instance: MongoLogger) -> None:
    """
    Handles movie search by keyword with pagination.
    Args:
        db: Instance of MovieDatabase for queries.
        logger_instance: Instance of MongoLogger for logging.
    """
    keyword: str = console.input("\n[bold cyan]Enter search keyword:[/bold cyan] ").strip()
    if not keyword: return
    offset: int = 0
    first_run: bool = True
    while True:
        results = db.search_by_title(keyword, offset)
        if first_run and not results:
            console.print(f"\n[bold yellow]No movies found matching: '{keyword}'[/bold yellow]")
            break
        if not first_run and not results:
            console.print("\n[bold yellow]End of results reached.[/bold yellow]")
            break
        fmt.display_movies(results)

        if offset == 0:
            logger_instance.save_search_log(
                                "keyword",
                                    {"keyword": keyword},
                                            len(results)
                                              )
        next_results = db.search_by_title(keyword, offset + 10)
        if not next_results:
            console.print("\n[bold yellow]  No more movies found.[/bold yellow]")
            break
        if console.input("\n[bold yellow]Load next 10 results? (y/n): [/bold yellow]").lower() != "y":
            break
        offset += 10
        first_run = False



def display_stats(stats: List[Any]) -> None:
    """
    Displays the top search statistics in a beautiful table format.
    Args:
        stats: A list of search statistics to display.
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
            table.add_row(f"[white]{idx}[/]", f"[cyan]{stat.keyword}[/]", f"[green]{stat.count}[/]")
    console.print(Panel(table, border_style="blue", expand=False))


def display_genres(genres: List[str]) -> None:
    """
    Displays genres in a beautiful, framed, multi-column table
    Args:
        genres: A list of genre names to display.
    """
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column(justify="left", style="bold cyan")
    table.add_column(justify="left", style="bold cyan")
    table.add_column(justify="left", style="bold cyan")

    for i in range(0, len(genres), 3):
        row = genres[i:i + 3]
        formatted_row = [f"[yellow]{idx + 1}.[/] [white]{genre.upper()}[/]" for idx, genre in enumerate(row, i)]
        while len(formatted_row) < 3:
            formatted_row.append("")
        table.add_row(*formatted_row)
    console.print(Panel(table, title="[bold magenta]SELECT A GENRE[/]", border_style="blue", expand=False))