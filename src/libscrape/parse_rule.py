"""
Library for managing parse rules for parsing raw data from scraped library pages. A parse rule is a 
collection of indexes associated with specific data points. Encapsulating these indexes within a ParseRule
object enables more maintainable code.
"""


class DurhamParseRule:
    """
    A generic parse rule with rules common to all library systems in Durham region

    Attributes
        - title: the index of the title
        - item_format: the index of the format of the library item
        - status_with_subtitle: the index of the library items hold/checkout status if the subtitle is included in the
            item's data
        - status_without_subtitle: the index of the library item's hold/checkout status if the subtitle isn't included
            in the item's data
        - item_date_with_subtitle: the index of the library item's pickup/return date if the subtitle is included in
            the item's data
        - item_date_without_subtitle: the index of the library item's pickup/return date if the subtitle isn't included
            in the item's data
    """

    def __init__(self, title, item_format, status_with_subtitle=None, status_without_subtitle=None,
                 item_date_with_subtitle=None, item_date_without_subtitle=None):
        self.title = title
        self.format = item_format
        self.status_with_subtitle = status_with_subtitle
        self.status_without_subtitle = status_without_subtitle
        self.item_date_with_subtitle = item_date_with_subtitle
        self.item_date_without_subtitle = item_date_without_subtitle


class DurhamDVDHoldRule(DurhamParseRule):
    """
    Parse rule for DVDs on hold at any library system in Durham region

    Attributes
        - title: the index of the title
        - item_format: the index of the format of the library item
        - status_with_subtitle: the index of the library items hold/checkout status if the subtitle is included in the
            item's data
        - status_without_subtitle: the index of the library item's hold/checkout status if the subtitle isn't included
            in the item's data
        - item_date_with_subtitle: the index of the library item's pickup/return date if the subtitle is included in
            the item's data
        - item_date_without_subtitle: the index of the library item's pickup/return date if the subtitle isn't included
            in the item's data
        - branch_with_subtitle: the index of the library item's pickup branch location if the subtitle is included in
            the item's data
        - branch_without_subtitle: the index of the library item's pickup branch location if the subtitle isn't included
            in the item's data
    """

    def __init__(self, title, item_format, status_with_subtitle=None, status_without_subtitle=None,
                 item_date_with_subtitle=None, item_date_without_subtitle=None, branch_with_subtitle=None,
                 branch_without_subtitle=None):
        super().__init__(title, item_format, status_with_subtitle, status_without_subtitle, item_date_with_subtitle,
                         item_date_without_subtitle)
        self.branch_with_subtitle = branch_with_subtitle
        self.branch_without_subtitle = branch_without_subtitle


class DurhamDVDCheckoutRule(DurhamParseRule):
    """
    Parse rule for checkout items with a generic format of DVD in Durham Region library systems

    Attributes
        - title: the index of the title
        - item_format: the index of the format of the library item
        - status_with_subtitle: the index of the library items checkout status if the subtitle is included in the
            item's data
        - status_without_subtitle: the index of the library item's checkout status if the subtitle isn't included
            in the item's data
        - item_date_with_subtitle: the index of the library item's return date if the subtitle is included in
            the item's data
        - item_date_without_subtitle: the index of the library item's return date if the subtitle isn't included
            in the item's data
    """

    def __init__(self, title, item_format, status_with_subtitle=None, status_without_subtitle=None,
                 item_date_with_subtitle=None, item_date_without_subtitle=None):
        super().__init__(title, item_format, status_with_subtitle, status_without_subtitle, item_date_with_subtitle,
                         item_date_without_subtitle)


class DurhamBookAndCDHoldRule(DurhamParseRule):
    """
    Parse rule for library items on hold with a generic format of Book or CD at any library system in Durham region

    Attributes
        - title: the index of the title
        - item_format: the index of the format of the library item
        - contributors_with_subtitle: the index of the library item's contributors if the subtitle is included in the
            item's data
        - contributors_without_subtitle: the index of the library item's contributors if the subtitle isn't included
            in the item's data
        - status_with_subtitle: the index of the library items hold/checkout status if the subtitle is included in the
            item's data
        - status_without_subtitle: the index of the library item's hold/checkout status if the subtitle isn't included
            in the item's data
        - item_date_with_subtitle: the index of the library item's pickup/return date if the subtitle is included in
            the item's data
        - item_date_without_subtitle: the index of the library item's pickup/return date if the subtitle isn't included
            in the item's data
        - branch_with_subtitle: the index of the library item's pickup branch location if the subtitle is included in
            the item's data
        - branch_without_subtitle: the index of the library item's pickup branch location if the subtitle isn't included
            in the item's data
    """

    def __init__(self, title, item_format, contributors_with_subtitle=None, contributors_without_subtitle=None,
                 status_with_subtitle=None, status_without_subtitle=None,
                 item_date_with_subtitle=None, item_date_without_subtitle=None, branch_with_subtitle=None,
                 branch_without_subtitle=None):
        super().__init__(title, item_format, status_with_subtitle, status_without_subtitle, item_date_with_subtitle,
                         item_date_without_subtitle)
        self.contributors_with_subtitle = contributors_with_subtitle
        self.contributors_without_subtitle = contributors_without_subtitle
        self.branch_with_subtitle = branch_with_subtitle
        self.branch_without_subtitle = branch_without_subtitle


class DurhamBookAndCDCheckoutRule(DurhamParseRule):
    """
    Parse rule for checkout items with a generic format of Book or CD in Durham Region library systems

    Attributes
        - title: the index of the title
        - item_format: the index of the format of the library item
        - contributors_with_subtitle: the index of the library item's contributors if the subtitle is included in the
            item's data
        - contributors_without_subtitle: the index of the library item's contributors if the subtitle isn't included
            in the item's data
        - status_with_subtitle: the index of the library items checkout status if the subtitle is included in the
            item's data
        - status_without_subtitle: the index of the library item's checkout status if the subtitle isn't included
            in the item's data
        - item_date_with_subtitle: the index of the library item's return date if the subtitle is included in
            the item's data
        - item_date_without_subtitle: the index of the library item's return date if the subtitle isn't included
            in the item's data
    """

    def __init__(self, title, item_format, contributors_with_subtitle=None, contributors_without_subtitle=None,
                 status_with_subtitle=None, status_without_subtitle=None,
                 item_date_with_subtitle=None, item_date_without_subtitle=None):
        super().__init__(title, item_format, status_with_subtitle, status_without_subtitle, item_date_with_subtitle,
                         item_date_without_subtitle)
        self.contributors_with_subtitle = contributors_with_subtitle
        self.contributors_without_subtitle = contributors_without_subtitle


class TorontoParseRule:
    """
    A generic parse rule with rules relevant to all items in the Toronto Public Library system

    Attributes
        - title: the index of the title
        - item_format: the index of the format of the library item
        - contributors: the index of the library item's contributors
        - status: the index of the library item's pickup/return status
        - item_date: the index of the library item's pickup/return date
    """

    def __init__(self, title, item_format, contributors, status, item_date):
        self.title = title
        self.item_format = item_format
        self.contributors = contributors
        self.status = status
        self.item_date = item_date


class TorontoCheckoutParseRule(TorontoParseRule):
    """
    Parse rule for Toronto Public Library checkout items

    Attributes
        - title: the index of the title
        - item_format: the index of the format of the library item
        - contributors: the index of the library item's contributors
        - status: the index of the library item's return status
        - item_date: the index of the library item's return date
    """

    def __init__(self, title, item_format, contributors, status, item_date):
        super().__init__(title, item_format, contributors, status, item_date)


class TorontoHoldParseRule(TorontoParseRule):
    """
    Parse rule for Toronto Public Library items on hold

    Attributes
        - title: the index of the title
        - item_format: the index of the format of the library item
        - contributors: the index of the library item's contributors
        - status: the index of the library item's hold status
        - item_date: the index of the library item's pickup date
        - branch: the index of the pickup location for a library item
    """

    def __init__(self, title, item_format, contributors, item_date, branch):
        super().__init__(title, item_format, contributors, None, item_date)
        self.branch = branch
