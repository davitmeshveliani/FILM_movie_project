from functools import wraps
from typing import Callable, Any, Optional

def safe_execution(logger: Any) -> Callable[[Callable], Callable]:
    """
    Decorator factory that provides centralized error handling and logging.

    Args:
        logger (Any): An instance of a logger capable of handling error logs.

    Returns:
        Callable: A decorator that wraps the target function with try-except logic.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Optional[Any]:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"\nSystem error in {func.__name__}: {e}")
                if hasattr(logger, 'error'):
                    logger.error(f"Error in {func.__name__}: {e}")
                return None
        return wrapper
    return decorator

class InvalidYearError(Exception):
    """
    Custom exception raised when a provided year is outside realistic bounds
    """
    pass