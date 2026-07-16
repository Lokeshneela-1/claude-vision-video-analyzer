"""
Utility functions for logging and output formatting.
"""

import logging
import sys
from colorama import Fore, Style, init

# Initialize colorama for cross-platform colored output
init(autoreset=True)


def setup_logging(verbose: bool = False) -> logging.Logger:
    """
    Setup logging configuration.
    
    Args:
        verbose: Enable verbose logging
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger("video_analyzer")
    
    # Remove existing handlers
    logger.handlers = []
    
    # Set log level
    level = logging.DEBUG if verbose else logging.INFO
    logger.setLevel(level)
    
    # Create console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    
    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(handler)
    
    return logger


def print_header(text: str) -> None:
    """Print a formatted header."""
    print(f"\n{Fore.CYAN}{'=' * 60}")
    print(f"{Fore.CYAN}{text.center(60)}")
    print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}\n")


def print_success(text: str) -> None:
    """Print success message in green."""
    print(f"{Fore.GREEN}{text}{Style.RESET_ALL}")


def print_error(text: str) -> None:
    """Print error message in red."""
    print(f"{Fore.RED}{text}{Style.RESET_ALL}", file=sys.stderr)


def print_info(text: str, end: str = "\n") -> None:
    """Print info message in blue."""
    print(f"{Fore.BLUE}{text}{Style.RESET_ALL}", end=end)


def print_warning(text: str) -> None:
    """Print warning message in yellow."""
    print(f"{Fore.YELLOW}{text}{Style.RESET_ALL}")
