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
    return input("\nSelection: ").strip()


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
        choice = input("\nGenre Name or Number: ").strip().lower()

        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(genres):
                return genres[idx]
        if choice in genres_lower:
            return genres[genres_lower.index(choice)]
        print(f"Invalid input. Please choose 1-{len(genres)} or type the full name.")


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
            start = input(f"Start Year (min {min_y}): ").strip()
            end = input(f"End Year (max {max_y}): ").strip()

            y_from = int(start) if start else min_y
            y_to = int(end) if end else max_y

            if not (min_y <= y_from <= max_y and min_y <= y_to <= max_y):
                raise InvalidYearError(f"Years must be between {min_y} and {max_y}.")

            if y_from > y_to:
                raise InvalidYearError("Start year cannot be greater than end year.")
            return y_from, y_to

        except ValueError:
            print("Error: Invalid input! Please enter valid numbers.")
        except InvalidYearError as e:
            print(f"Business Logic Error: {e}")


def handle_genre_search(db: MovieDatabase, logger: MongoLogger, min_y: int, max_y: int) -> None:
    """
    Orchestrates the user flow for searching movies by genre and year.
    Args:
        db: Instance of MovieDatabase for queries.
        logger: Instance of MongoLogger for saving activity.
        min_y: The lower bound for the search years.
        max_y: The upper bound for the search years.
    """
    genres = db.get_genres()
    display_genres(genres)

    genre = get_valid_genre(genres)
    y_from, y_to = get_valid_year_range(min_y, max_y)

    offset = 0
    while True:
        results = db.search_by_genre_year(genre, y_from, y_to, offset)
        if not results:
            print("\nNo results found for your criteria.")
            break

        fmt.display_movies(results)
        if offset == 0:
            logger.save_search_log("genre_year", {"genre": genre, "from": y_from, "to": y_to}, len(results))
        if len(results) < 10 or input("\nLoad next 10? (y/n): ").lower() != 'y':
            break
        offset += 10


def handle_keyword_search(db: MovieDatabase, logger_instance: MongoLogger) -> None:
    """
    Handles movie search by keyword with pagination.
    Args:
        db: Instance of MovieDatabase for queries.
        logger_instance: Instance of MongoLogger for logging.
    """
    keyword: str = input("\nEnter search keyword: ").strip()
    if not keyword: return

    offset: int = 0
    first_run: bool = True
    while True:
        results = db.search_by_title(keyword, offset)
        if first_run and not results:
            print(f"\nNo movies found matching !: '{keyword}'")
            break
        if not first_run and not results:
            print("\nEnd of results reached.!")
            break

        fmt.display_movies(results)
        if offset == 0 and results:
            logger_instance.save_search_log("keyword", {"keyword": keyword}, len(results))

        if len(results) < 10:
            print("\n End of results.")
            break
        if input("\nLoad next 10 results? (y/n): ").lower() != 'y':
            break
        offset += 10


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