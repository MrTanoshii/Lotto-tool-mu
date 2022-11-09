from datetime import date


class TicketEntry(object):
    """Base entry for ticket entries."""

    def __init__(self, start_date: date, end_date: date, lotto_num: list[int]):
        """Constructor.

        Keyword Arguments:
        start_date: date -- The start date of the entry.
        end_date: date -- The end date of the entry.
        lotto_num: list[int] -- The lotto numbers."""

        self.start_date: date = start_date
        self.end_date: date = end_date
        self.lotto_num: list[int] = lotto_num

    def __str__(self) -> str:
        """String representation."""

        return f"Valid from {self.start_date} to {self.end_date} | Numbers: {self.lotto_num}"
