from datetime import date, timedelta
from pathlib import Path
from typing import Optional, TYPE_CHECKING


# Local modules
from src.const.const import Const
from src.tools.ticket_entry import TicketEntry
from src.tools.draw_result import DrawResult

# Fix typing circular imports
if TYPE_CHECKING:
    from src.tools.scraper import Scraper


class Checker(object):
    """Base class for lotto checker."""

    def __init__(self):
        """Constructor."""

        self.draw_results_path: Path = Path("./data/draw_results.txt")
        self.ticket_entries_path: Path = Path("./data/ticket_entries.txt")

    def get_draw_result_by_date(self, draw_date: date) -> Optional[DrawResult]:
        """Get the draw result by date.

        Keyword Arguments:
        draw_date: date -- The date of the draw.

        Returns:
        Optional[DrawResult] -- The winning draw result."""

        if self.draw_results_path.exists():
            with open(self.draw_results_path, "r") as file:
                for line in file:
                    line = line.strip()
                    if line.startswith(str(draw_date)):
                        winning_num_str: list[str] = line.split(", ")
                        winning_num: list[int] = []
                        if len(winning_num_str) == 7:
                            winning_num = [int(num) for num in winning_num_str[1:]]
                        return DrawResult(draw_date, winning_num)

        return None

    def check_entry(self, scraper: "Scraper", ticket_entry: TicketEntry) -> list[bool]:
        """Check the ticket entry against draw results.

        Keyword Arguments:
        scraper: Scraper -- The scraper object.
        ticket_entry: TicketEntry -- The ticket entry to check.

        Returns:
        list[bool] -- True if the ticket entry won the jackpot, False otherwise."""

        results: list[bool] = []
        date_delta = timedelta(days=1)

        # iterate over range of dates
        current_date: date = ticket_entry.start_date
        while current_date <= ticket_entry.end_date:
            draw_result: DrawResult = scraper.get_draw_result_by_date(
                self, current_date
            )
            if draw_result is not None:
                num: int
                won: bool = True
                for num in ticket_entry.lotto_num:
                    if num not in draw_result.winning_num:
                        won = False
                        break
                results.append(won)

            # Next day
            current_date += date_delta

        return results

    def check_entry_from_file(self, scraper: "Scraper") -> None:
        """Check ticket entries from file against draw results.

        Keyword Arguments:
        scraper: Scraper -- The scraper object."""

        if self.ticket_entries_path.exists():
            with open(self.ticket_entries_path, "r") as file:
                line: str
                for line in file:
                    line = line.strip()
                    split_line: list[str] = line.split(", ")

                    start_date: date = self._get_date_from_str(split_line[0])
                    end_date: date = self._get_date_from_str(split_line[1])

                    ticket_entry: TicketEntry = TicketEntry(
                        start_date, end_date, list(map(int, split_line[2::]))
                    )
                    win_list: list[bool] = self.check_entry(scraper, ticket_entry)
                    print(ticket_entry)
                    for win in win_list:
                        # Color result
                        if win:
                            print(Const.COLOR.GREEN, end="")
                        else:
                            print(Const.COLOR.DARK_GREY, end="")

                        print(f"{win}{Const.COLOR.RESET}", end=" ")
                    print("\n")

    def _get_date_from_str(self, date_str: str) -> date:
        """Get date from string.

        Keyword Arguments:
        date_str: str -- The date string. Format: YYYY-MM-DD.

        Returns:
        date -- The date."""

        date_list_str: list[str] = date_str.split("-")
        return date(
            int(date_list_str[0]),
            int(date_list_str[1]),
            int(date_list_str[2]),
        )
