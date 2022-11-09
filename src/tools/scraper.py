from bs4 import BeautifulSoup
import bs4
from datetime import date
from pathlib import Path
import requests
from typing import Optional, Union

# Local modules
from src.const.const import Const
from src.tools.checker import Checker
from src.tools.ticket_entry import TicketEntry
from src.tools.draw_result import DrawResult


class Scraper(object):
    """Base class for web scraping."""

    def __init__(
        self,
        url: str = "https://www.loterienationale.mu/fr/tirages-et-archives",
    ):
        """Constructor."""

        self._url: str = url
        self._request: str = ""
        self._soup: BeautifulSoup = None
        self.draw_results_path: Path = Path("./data/draw_results.txt")
        self.ticket_entries_path: Path = Path("./data/ticket_entries.txt")

    def _get_soup(self) -> None:
        """Get the soup."""

        response: requests.Response = requests.get(self._url + self._request)
        self._soup = BeautifulSoup(response.text, "html.parser")

    def _get_tag_by_id(self, id: str) -> Union[bs4.Tag, bs4.NavigableString, None]:
        """Get the text from a tag and class.

        Keyword Arguments:
        id: str -- The id of the tag.

        Returns:
        : Tag | NavigableString | None"""

        return self._soup.find(id=id)

    def get_draw_result_by_date(
        self, checker: Checker, draw_date: date
    ) -> Optional[DrawResult]:
        """Get the draw result by date.

        Keyword Arguments:
        checker: Checker -- The checker object.
        draw_date: date -- The date of the draw.

        Returns:
        : Optional[DrawResult] -- The winning draw result."""

        # Try to get results from local file if available
        draw_result: Optional[DrawResult] = checker.get_draw_result_by_date(draw_date)
        if draw_result is not None:
            return draw_result

        # Try to get results from scraping
        self._request = f"?field_date_du_tirage_value[value][date]={draw_date.day}%20{Const.MONTH.MONTH_NAME_SHORT[draw_date.month - 1]}%20{draw_date.year}"
        self._get_soup()

        result = self._get_tag_by_id("num-gagnants")
        # Found results
        if type(result) == bs4.Tag:
            winning_num_str: Union[bs4.Tag, bs4.NavigableString, None] = result.text
            winning_num: list[int] = [int(num) for num in winning_num_str.split(", ")]
            draw_result = DrawResult(draw_date, winning_num)

        if draw_result is None:
            print(
                f"{Const.COLOR.RED}Error{Const.COLOR.RESET}: No result found for {draw_date.isoformat()}"
            )
            draw_result = DrawResult(draw_date)

        self.save_results(draw_result)
        return draw_result

    def save_entry(self, ticket_entry: TicketEntry) -> None:
        """Save the ticket entry.

        Keyword Arguments:
        ticket_entry: TicketEntry -- The ticket entry."""

        with open(self.ticket_entries_path, "a") as tmp_file:
            tmp_str: str = ""
            tmp_str += f"{ticket_entry.start_date}, {ticket_entry.end_date}, "
            for i in ticket_entry.lotto_num:
                tmp_str += f"{i}, "
            tmp_str = tmp_str[:-2]
            tmp_file.write(f"{tmp_str}\n")

    def save_results(self, draw_result: DrawResult) -> None:
        """Save the draw results.

        Keyword Arguments:
        draw_result: DrawResult -- The draw result."""

        with open(self.draw_results_path, "a") as tmp_file:
            tmp_str: str = ""
            tmp_str += f"{draw_result.draw_date}, "
            if len(draw_result.winning_num) > 0:
                for i in draw_result.winning_num:
                    tmp_str += f"{i}, "
            else:
                tmp_str += "NOT_FOUND, "
            tmp_str = tmp_str[:-2]
            tmp_file.write(f"{tmp_str}\n")
