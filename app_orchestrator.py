import ui_handlers as ui
from decorators import safe_execution


class AppOrchestrator:
    """
    Orchestrates the application workflow, mapping menu choices to UI handlers
    and ensuring safe execution of operations via decorators.
    """
    def __init__(self, db, log, analytics):
        """
        Initializes the orchestrator with database, logger, and analytics instances.

        Args:
            db (Any): The database manager instance.
            log (Any): The logger instance for recording search activity.
            analytics (Any): The analytics engine instance for report generation.
        """
        self.db = db
        self.log = log
        self.analytics = analytics

        min_y, max_y = self.db.get_year_range()
        safe_run = safe_execution(self.log)

        self.menu = {
            "1": lambda: safe_run(ui.handle_keyword_search)(self.db, self.log),
            "2": lambda: safe_run(ui.handle_genre_search)(self.db, self.log, min_y, max_y),
            "3": lambda: safe_run(ui.display_stats)(self.analytics.get_popular_searches())
        }

    def run(self):
        """
        Runs the main application loop, handling user input and menu navigation.

        The loop continues until the user selects '4' (Exit)
        """
        while True:
            choice = ui.display_menu()
            if choice == '4':
                print("\nThank you from Davit. Goodbye!")
                break
            if action := self.menu.get(choice):
                action()
            else:
                print("\nInvalid input. Please try again.")