# Local modules
from src.tools.checker import Checker
from src.tools.scraper import Scraper

if __name__ == "__main__":
    scraper: Scraper = Scraper()
    checker: Checker = Checker()

    checker.check_entry_from_file(scraper)
