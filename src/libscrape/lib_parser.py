"""
Library for managing applying parse rules to raw data from scraped library pages.
"""

import re
from abc import ABC, abstractmethod


class LibraryParser(ABC):
    """
    An abstract LibraryParser that outlines the required methods
    for a concrete Parser class for any library system

    Attributes:
     - parse_rule: the rules this parser will use to process data scraped from a libraries website
    """

    def __init__(self, parse_rule):
        self.parse_rule = parse_rule

    @abstractmethod
    def title(self, data_to_parse):
        pass

    @abstractmethod
    def format(self, data_to_parse):
        pass

    @abstractmethod
    def contributors(self, data_to_parse):
        pass


class DurhamParser(LibraryParser):
    """
    A concrete LibraryParser with common functionalities among libraries within Durham Region

    Attributes:
      - parse_rule: the rules this parser will use to
    """

    def __init__(self, parse_rule):
        super().__init__(parse_rule)

    def title(self, data_to_parse):
        """
        Get the title of a single library item from a Durham Region library system

        Parameters
        ----------
        data_to_parse: list of strings generated by splitting the scraped text of a single library item by the new
        line character

        Returns
        -------
        A string representing the title of the library item
        """
        return data_to_parse[self.parse_rule.title].rsplit(", ", 1)[0]

    def format(self, data_to_parse):
        """
        Get the item format of a single library item from a Durham Region library system

        Parameters
        ----------
        data_to_parse: list of strings generated by splitting the scraped text of a single library item by the new
        line character

        Returns
        -------
        A string representing the format of the library item (e.g. DVD, Book, CD, etc.)
        """
        return data_to_parse[self.parse_rule.item_format].rsplit(", ", 1)[1]

    @staticmethod
    def format(data_to_parse):
        """
        Statically get the item format of a single library item from a Durham Region library system

        Parameters
        ----------
        data_to_parse: list of strings generated by splitting the scraped text of a single library item by the new
        line character

        Returns
        -------
        A string representing the format of the library item (e.g. DVD, Book, CD, etc.)
        """
        return data_to_parse[2].rsplit(", ", 1)[1]

    @staticmethod
    def title(data_to_parse):
        """
        Statically get the title of a single library item from a Durham Region library system

        Parameters
        ----------
        data_to_parse: list of strings generated by splitting the scraped text of a single library item by the new
        line character

        Returns
        -------
        A string representing the title of the library item
        """
        return data_to_parse[2].rsplit(", ", 1)[0]

    def contributors(self, data_to_parse, generic_format, has_subtitle=None):
        """
        Get the contributors (e.g. authors, directors, etc.) of a single library item from a Durham Region library
        system

        Parameters
        ----------
        data_to_parse: list of strings generated by splitting the scraped text of a single library item by the new
        line character
        generic_format: the common item format that this item belongs to. For example, a "Book Set" would have a
            generic format of "Book"
        has_subtitle: a boolean that indicates if data_to_parse contains subtitle data

        Returns
        -------
        A string representing the contributors of the library item
        """
        if generic_format == "DVD":
            return ""

        if has_subtitle is None:
            has_subtitle = DurhamHoldParser.has_subtitle(data_to_parse)

        if has_subtitle:
            return data_to_parse[self.parse_rule.contributors_with_subtitle]
        else:
            return data_to_parse[self.parse_rule.contributors_without_subtitle]


class DurhamHoldParser(DurhamParser):
    """
    A concrete Durham Region LibraryParser specialized for parsing library items on hold

    Attributes:
      - parse_rule: the rules this parser will use to
    """

    def __init__(self, parse_rule):
        super().__init__(parse_rule)

    @staticmethod
    def has_subtitle(data_to_parse, item_format=None):
        """
        Statically determine if the library item data contains subtitle data

        Parameters
        ----------
        data_to_parse: list of strings generated by splitting the scraped text of a single library item by the new
        line character
        item_format: the specific format of the library item

        Returns
        -------
        True if data_to_parse contains subtitle data, False otherwise
        """
        if not item_format:
            item_format = DurhamHoldParser.format(data_to_parse)
        if item_format == "DVD":
            return not (data_to_parse[4][:2] == 'by') and not (data_to_parse[4][:6] == 'DVD - ')
        elif item_format == "CD" or item_format == "Book":
            return not (data_to_parse[4][:2] == 'by')

    def status(self, data_to_parse, has_subtitle=None):
        """
        Get the hold status of the library item

        Parameters
        ----------
        data_to_parse: list of strings generated by splitting the scraped text of a single library item by the new
        line character
        has_subtitle: a boolean that indicates if data_to_parse contains subtitle data

        Returns
        -------
        A string representing the hold status of the library item
        """
        if has_subtitle is None:
            has_subtitle = DurhamHoldParser.has_subtitle(data_to_parse)

        if has_subtitle:
            status = data_to_parse[self.parse_rule.status_with_subtitle]
        else:
            status = data_to_parse[self.parse_rule.status_without_subtitle]

        if "Not ready" in status:
            return "Not Ready"
        else:
            return "Ready"

    def item_date(self, data_to_parse, has_subtitle=None):
        """
        Get the pick-up date of the library item

        Parameters
        ----------
        data_to_parse: list of strings generated by splitting the scraped text of a single library item by the new
        line character
        has_subtitle: a boolean that indicates if data_to_parse contains subtitle data

        Returns
        -------
        A string representing the pick-up date of the library item
        """
        if has_subtitle is None:
            has_subtitle = DurhamHoldParser.has_subtitle(data_to_parse)

        if has_subtitle:
            item_date = data_to_parse[self.parse_rule.item_date_with_subtitle]
        else:
            item_date = data_to_parse[self.parse_rule.item_date_without_subtitle]

        if "Expires on " in item_date:
            item_date = item_date.replace("Expires on ", "")
        elif "Pick up by " in item_date:
            item_date = item_date.replace("Pick up by", "")

        return item_date

    def branch(self, data_to_parse, has_subtitle=None):
        """
        Get the name of the library branch that this library item should be picked up at

        Parameters
        ----------
        data_to_parse: list of strings generated by splitting the scraped text of a single library item by the new
        line character
        has_subtitle: a boolean that indicates if data_to_parse contains subtitle data

        Returns
        -------
        A string representing the branch where this library item on hold should be picked up
        """
        if has_subtitle is None:
            has_subtitle = DurhamHoldParser.has_subtitle(data_to_parse)

        if has_subtitle:
            branch = data_to_parse[self.parse_rule.branch_with_subtitle]
        else:
            branch = data_to_parse[self.parse_rule.branch_without_subtitle]

        return branch.replace("Pick up by ", "")

    def all(self, data_to_parse, generic_format, has_subtitle=None):
        """
        Gets all relevant data (title, format, contributors, status, pick up date, pick up branch) of this library item

        Parameters
        ----------
        data_to_parse: list of strings generated by splitting the scraped text of a single library item by the new
            line character
        generic_format: the common item format that this item belongs to. For example, a "Book Set" would have a
            generic format of "Book"
        has_subtitle: a boolean that indicates if data_to_parse contains subtitle data

        Returns
        -------
        A list containing all relevant data of this library item
        """
        if not has_subtitle:
            has_subtitle = DurhamHoldParser.has_subtitle(data_to_parse, generic_format)

        return [
            self.title(data_to_parse),
            self.format(data_to_parse),
            self.contributors(data_to_parse, generic_format, has_subtitle),
            self.status(data_to_parse, has_subtitle),
            self.item_date(data_to_parse, has_subtitle),
            self.branch(data_to_parse, has_subtitle)
        ]


class DurhamCheckoutParser(DurhamParser):
    """
    A concrete Durham Region LibraryParser specialized for parsing library items checked out

    Attributes:
      - parse_rule: the rules this parser will use to
    """

    def __init__(self, parse_rule):
        super().__init__(parse_rule)

    @staticmethod
    def has_subtitle(data_to_parse, item_format=None):
        """
        Statically determine if the library item data contains subtitle data

        Parameters
        ----------
        data_to_parse: list of strings generated by splitting the scraped text of a single library item by the new
        line character
        item_format: the specific format of the library item

        Returns
        -------
        True if data_to_parse contains subtitle data, False otherwise
        """
        if not item_format:
            item_format = DurhamCheckoutParser.format(data_to_parse)
        if "CD" in item_format:
            if data_to_parse[3][:2] == 'by':
                return len(data_to_parse) > 15
            else:
                return len(data_to_parse) > 14

        elif "Book" in item_format:
            return len(data_to_parse) > 15

        elif "DVD" in item_format:
            return len(data_to_parse) > 14
        else:
            return False

    def status(self, data_to_parse, has_subtitle=None):
        """
        Get the checkout status of this library item

        Parameters
        ----------
        data_to_parse: list of strings generated by splitting the scraped text of a single library item by the new
        line character
        has_subtitle: a boolean that indicates if data_to_parse contains subtitle data

        Returns
        -------
        A string representing the checkout status of this library item
        """
        if has_subtitle is None:
            has_subtitle = DurhamCheckoutParser.has_subtitle(data_to_parse)

        if has_subtitle:
            status = data_to_parse[self.parse_rule.status_with_subtitle]
        else:
            status = data_to_parse[self.parse_rule.status_without_subtitle]

        if "Due soon" in status:
            return "Due Soon"
        elif "Due later" in status:
            return "Due Later"
        else:
            return "Overdue"

    def item_date(self, data_to_parse, has_subtitle=None):
        """
        Get the date that this library item should be returned to the library

        Parameters
        ----------
        data_to_parse: list of strings generated by splitting the scraped text of a single library item by the new
        line character
        has_subtitle: a boolean that indicates if data_to_parse contains subtitle data

        Returns
        -------
        A string representing the date that this library item should be returned to the library
        """
        if has_subtitle is None:
            has_subtitle = DurhamHoldParser.has_subtitle(data_to_parse)

        if has_subtitle:
            item_date = data_to_parse[self.parse_rule.item_date_with_subtitle]
        else:
            item_date = data_to_parse[self.parse_rule.item_date_without_subtitle]

        item_date = item_date.replace("Due by ", "")

        return item_date

    def all(self, data_to_parse, generic_format, has_subtitle=None):
        """
        Gets all relevant data (title, format, contributors, checkout status) of this library item

        Parameters
        ----------
        data_to_parse: list of strings generated by splitting the scraped text of a single library item by the new
            line character
        generic_format: the common item format that this item belongs to. For example, a "Book Set" would have a
            generic format of "Book"
        has_subtitle: a boolean that indicates if data_to_parse contains subtitle data

        Returns
        -------
        A list containing all relevant data of this library item
        """
        if not has_subtitle:
            has_subtitle = DurhamCheckoutParser.has_subtitle(data_to_parse)
        return [
            self.title(data_to_parse),
            self.format(data_to_parse),
            self.contributors(data_to_parse, generic_format, has_subtitle),
            self.status(data_to_parse, has_subtitle),
            self.item_date(data_to_parse, has_subtitle)
        ]


class TorontoParser(LibraryParser):
    """
    A concrete Toronto Public Library LibraryParser

    Attributes:
        - parse_rule: the rules this parser will use to
    """

    def __init__(self, parse_rule):
        super().__init__(parse_rule)

    def title(self, data_to_parse):
        """
        Get the title of this library item

        Parameters
        ----------
        data_to_parse: list of strings generated by splitting the scraped text of a single library item by the new
            line character

        Returns
        -------
        A string representing the title of this library item
        """
        return data_to_parse[self.parse_rule.title]

    def format(self, data_to_parse):
        """
        Get the format of this library item

        Parameters
        ----------
        data_to_parse: list of strings generated by splitting the scraped text of a single library item by the new
            line character

        Returns
        -------
        A string representing the format of this library item
        """
        return data_to_parse[self.parse_rule.item_format]

    def contributors(self, data_to_parse):
        """
        Get the contributors of this library item

        Parameters
        ----------
        data_to_parse: list of strings generated by splitting the scraped text of a single library item by the new
            line character

        Returns
        -------
        A string representing the contributors of this library item
        """
        return data_to_parse[self.parse_rule.contributors]

    def item_date(self, data_to_parse):
        """
        Get the return or pickup date of this library item

        Parameters
        ----------
        data_to_parse: list of strings generated by splitting the scraped text of a single library item by the new
            line character

        Returns
        -------
        A string representing the return or pickup date of this library item
        """
        return data_to_parse[self.parse_rule.item_date]


class TorontoHoldParser(TorontoParser):
    """
    A concrete Toronto Public Library LibraryParser specialized for parsing library items on hold

    Attributes:
      - parse_rule: the rules this parser will use to
    """

    def __init__(self, parse_rule):
        super().__init__(parse_rule)

    def branch(self, data_to_parse):
        """
        Get the pickup branch for this library item

        Parameters
        ----------
        data_to_parse: list of strings generated by splitting the scraped text of a single library item by the new
            line character

        Returns
        -------
        A string representing the pickup branch of this library item
        """
        return data_to_parse[self.parse_rule.branch]

    def all(self, data_to_parse):
        """
        Gets all relevant data (title, format, contributors, pickup date, hold status, pickup location) of this library
        item

        Parameters
        ----------
        data_to_parse: list of strings generated by splitting the scraped text of a single library item by the new
            line character

        Returns
        -------
        A list of strings containing all the relevant data for this library item
        """
        return [self.title(data_to_parse), self.format(data_to_parse), self.contributors(data_to_parse),
                self.item_date(data_to_parse), 'Ready', self.branch(data_to_parse)]


class TorontoCheckoutParser(TorontoParser):
    """
    A concrete Toronto Public Library LibraryParser specialized for parsing library items checked out

    Attributes:
      - parse_rule: the rules this parser will use to
    """

    def __init__(self, parse_rule):
        super().__init__(parse_rule)

    def item_date(self, data_to_parse):
        """
        Get the return date for this library item

        Parameters
        ----------
        data_to_parse: list of strings generated by splitting the scraped text of a single library item by the new
            line character

        Returns
        -------
        A string representing the return date fot this library item
        """
        res = re.search('(?i)renew', data_to_parse[-1])
        if res:
            return data_to_parse[self.parse_rule.item_date - 2]
        else:
            return data_to_parse[self.parse_rule.item_date]

    def status(self, data_to_parse):
        """
        Get the checkout status of this library item

        Parameters
        ----------
        data_to_parse: list of strings generated by splitting the scraped text of a single library item by the new
            line character

        Returns
        -------
        A string representing the checkout status of this library item
        """
        status = data_to_parse[self.parse_rule.status]
        res = re.search('(?i)due', status)
        if res:
            return status
        else:
            return "Due Later"

    def all(self, data_to_parse):
        """
        Gets all relevant data (title, format, contributors, return date, checkout status) of this library
        item

        Parameters
        ----------
        data_to_parse: list of strings generated by splitting the scraped text of a single library item by the new
            line character

        Returns
        -------
        A list of strings containing all the relevant data for this library item
        """
        return [self.title(data_to_parse), self.format(data_to_parse), self.contributors(data_to_parse),
                self.item_date(data_to_parse), self.status(data_to_parse)]
