from datetime import date


class DrawResult(object):
    """Base class for draw results."""

    def __init__(self, draw_date: date, winning_num: list[int] = []) -> None:
        """Constructor.

        Keyword Arguments:
        draw_date: date -- The date of the draw.
        winning_num: list[int] -- The winning numbers (default: [])."""

        self.draw_date: date = draw_date
        self.winning_num: list[int] = winning_num

    def __str__(self) -> str:
        """String representation."""

        return f"{self.draw_date}: {self.winning_num}"
