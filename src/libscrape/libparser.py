from abc import ABC, abstractmethod
import re

# NOTE: ParserRule is just a dictionary that maps each expected piece of data
# to an index

# TODO: Apply a design pattern here
class ParseRule:
    def __init__(self, title, format):
        self.title = title
        self.format = format

class DurhamParseRule(ParseRule):
    def __init__(self,title, format,status_with_subtitle=None,status_without_subtitle=None, 
    item_date_with_subtitle=None,item_date_without_subtitle=None):
        super().__init__(title,format)
        self.status_with_subtitle=status_with_subtitle
        self.status_without_subtitle=status_without_subtitle
        self.item_date_with_subtitle=item_date_with_subtitle
        self.item_date_without_subtitle=item_date_without_subtitle

class TorontoParseRule(ParseRule):
    def __init__(self, title, format, contributors, status, item_date):
        super().__init__(title, format)
        self.contributors = contributors
        self.status = status
        self.item_date = item_date

class TorontoCheckoutParseRule(TorontoParseRule):
    def __init__(self, title, format, contributors, status, item_date):
        super().__init__(title, format, contributors, status, item_date)

class TorontoHoldParseRule(TorontoParseRule):
    def __init__(self, title, format, contributors, item_date, branch):
        super().__init__(title, format, contributors, None, item_date)
        self.branch = branch


class DurhamDVDHoldRule(DurhamParseRule):
    def __init__(self,title,format,status_with_subtitle=None,status_without_subtitle=None, 
    item_date_with_subtitle=None,item_date_without_subtitle=None,branch_with_subtitle=None,branch_without_subtitle=None):
        """
        title,format,contributors_with_subtitle,contributors_without_subtitle, status_with_subtitle,status_without_subtitle, 
        item_date_with_subtitle,item_date_without_subtitle,branch_with_subtitle,branch_without_subtitle
        """
        super().__init__(title,format,status_with_subtitle,status_without_subtitle,item_date_with_subtitle,item_date_without_subtitle)
        self.branch_with_subtitle=branch_with_subtitle
        self.branch_without_subtitle=branch_without_subtitle

class DurhamDVDCheckoutRule(DurhamParseRule):
    def __init__(self,title,format,status_with_subtitle=None,status_without_subtitle=None, 
    item_date_with_subtitle=None,item_date_without_subtitle=None):
        """
        title,format,contributors_with_subtitle,contributors_without_subtitle, status_with_subtitle,status_without_subtitle, 
        item_date_with_subtitle,item_date_without_subtitle,branch_with_subtitle,branch_without_subtitle
        """
        super().__init__(title,format,status_with_subtitle,status_without_subtitle,item_date_with_subtitle,item_date_without_subtitle)

class DurhamBookAndCDHoldRule(DurhamParseRule):
    def __init__(self,title,format,contributors_with_subtitle=None,contributors_without_subtitle=None, status_with_subtitle=None,status_without_subtitle=None, 
    item_date_with_subtitle=None,item_date_without_subtitle=None,branch_with_subtitle=None,branch_without_subtitle=None):
        """
        title,format,contributors_with_subtitle,contributors_without_subtitle, status_with_subtitle,status_without_subtitle, 
        item_date_with_subtitle,item_date_without_subtitle,branch_with_subtitle,branch_without_subtitle
        """
        super().__init__(title,format,status_with_subtitle,status_without_subtitle,item_date_with_subtitle,item_date_without_subtitle)
        self.contributors_with_subtitle=contributors_with_subtitle
        self.contributors_without_subtitle=contributors_without_subtitle
        self.branch_with_subtitle=branch_with_subtitle
        self.branch_without_subtitle=branch_without_subtitle

class DurhamBookAndCDCheckoutRule(DurhamParseRule):
    def __init__(self,title,format,contributors_with_subtitle=None,contributors_without_subtitle=None, status_with_subtitle=None,status_without_subtitle=None, 
    item_date_with_subtitle=None,item_date_without_subtitle=None):
        """
        title,format,contributors_with_subtitle,contributors_without_subtitle, status_with_subtitle,status_without_subtitle, 
        item_date_with_subtitle,item_date_without_subtitle,branch_with_subtitle,branch_without_subtitle
        """
        super().__init__(title,format,status_with_subtitle,status_without_subtitle,item_date_with_subtitle,item_date_without_subtitle)
        self.contributors_with_subtitle=contributors_with_subtitle
        self.contributors_without_subtitle=contributors_without_subtitle

class LibraryParser(ABC):
    def __init__(self, parse_rule):
        self.parse_rule = parse_rule

    '''Returns a title given a list of strings'''
    @abstractmethod
    def title(self, data_to_parse):
        pass

    '''Returns the format given a list of strings'''
    @abstractmethod
    def format(self, data_to_parse):
        pass

    '''Returns the contributors given a list of strings'''
    @abstractmethod
    def contributors(self, data_to_parse):
        pass

    '''Returns the status given a list of strings'''
    @abstractmethod
    def status(self, data_to_parse):
        pass
    '''Returns the date that the item should be picked up or returned'''
    @abstractmethod
    def item_date(self, data_to_parse, status=None):
        pass

class DurhamParser(LibraryParser):
    def __init__(self, parse_rule):
        super().__init__(parse_rule)

    def title(self, data_to_parse):
        return data_to_parse[self.parse_rule.title].rsplit(", ",1)[0]

    def format(self, data_to_parse):
        return data_to_parse[self.parse_rule.format].rsplit(", ",1)[1]

    @staticmethod
    def format(data_to_parse):
        return data_to_parse[2].rsplit(", ",1)[1]

    @staticmethod
    def title(data_to_parse):
        return data_to_parse[2].rsplit(", ",1)[0]

    def contributors(self, data_to_parse, generic_format, has_subtitle=None):
        if generic_format == "DVD":
            return ""

        if has_subtitle == None:
            has_subtitle = DurhamHoldParser.has_subtitle(data_to_parse)
       
        if has_subtitle:
            return data_to_parse[self.parse_rule.contributors_with_subtitle]
        else:
            return data_to_parse[self.parse_rule.contributors_without_subtitle]


class TorontoParser(LibraryParser):
    def __init__(self, parse_rule):
        super().__init__(parse_rule)

    def title(self, data_to_parse):
        return data_to_parse[self.parse_rule.title]

    def format(self, data_to_parse):
        return data_to_parse[self.parse_rule.format]

    def contributors(self, data_to_parse):
        return data_to_parse[self.parse_rule.contributors]

    def item_date(self, data_to_parse):
        return data_to_parse[self.parse_rule.item_date]
    

class TorontoHoldParser(TorontoParser):
    def __init__(self, parse_rule):
        super().__init__(parse_rule)

    def branch(self, data_to_parse):
        return data_to_parse[self.parse_rule.branch]
    
    def all(self, data_to_parse):
        return [self.title(data_to_parse), self.format(data_to_parse), self.contributors(data_to_parse), \
            self.item_date(data_to_parse), 'Ready', self.branch(data_to_parse)]

class TorontoCheckoutParser(TorontoParser):
    def __init__(self, parse_rule):
        super().__init__(parse_rule)

    def item_date(self, data_to_parse):
        res = re.search('(?i)renew', data_to_parse[-1])
        if res:
            return data_to_parse[self.parse_rule.item_date-2]
        else:
            return data_to_parse[self.parse_rule.item_date]
    def status(self, data_to_parse):
        status = data_to_parse[self.parse_rule.status]
        res = re.search('(?i)due', status)
        if res:
            return status
        else:
            return "Due Later"
    
    def all(self, data_to_parse):
        print(data_to_parse)
        print(self.title(data_to_parse))
        return [self.title(data_to_parse), self.format(data_to_parse), self.contributors(data_to_parse), \
            self.item_date(data_to_parse), self.status(data_to_parse)]


class DurhamHoldParser(DurhamParser):
    def __init__(self, parse_rule):
        super().__init__(parse_rule)

    @staticmethod
    def has_subtitle(data_to_parse, format=None):
        if not(format):
            format = DurhamHoldParser.format(data_to_parse)
        if format == "DVD":
            return not(data_to_parse[3][:2] == 'by') and not(data_to_parse[3][:6] == 'DVD - ')
        elif format == "CD" or format == "Book":
            return not(data_to_parse[3][:2] == 'by')

    def status(self, data_to_parse, has_subtitle=None):
        if has_subtitle == None:
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
        if has_subtitle == None:
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
        if has_subtitle == None:
            has_subtitle = DurhamHoldParser.has_subtitle(data_to_parse)
        
        if has_subtitle:
            branch = data_to_parse[self.parse_rule.branch_with_subtitle]
        else:
            branch = data_to_parse[self.parse_rule.branch_without_subtitle]
        
        return branch.replace("Pick up by ", "")

    def all(self, data_to_parse, generic_format, has_subtitle=None):
        if not(has_subtitle):
            has_subtitle = DurhamHoldParser.has_subtitle(data_to_parse,generic_format)

        return [
            self.title(data_to_parse), 
            self.format(data_to_parse), 
            self.contributors(data_to_parse,generic_format,has_subtitle), 
            self.status(data_to_parse,has_subtitle),
            self.item_date(data_to_parse,has_subtitle),
            self.branch(data_to_parse, has_subtitle)
            ]

class DurhamCheckoutParser(DurhamParser):
    def __init__(self, parse_rule):
        super().__init__(parse_rule)

    @staticmethod
    def has_subtitle(data_to_parse, format=None):
        if not(format):
            format = DurhamCheckoutParser.format(data_to_parse)
        if "CD" in format:
            if (data_to_parse[3][:2] == 'by'):
                    return len(data_to_parse) > 15
            else:
                return len(data_to_parse) > 14

        elif "Book" in format:
            return len(data_to_parse) > 15

        elif "DVD" in format:
            return len(data_to_parse) > 14
        else:
            return False

    def status(self, data_to_parse, has_subtitle=None):
        if has_subtitle == None:
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
        if has_subtitle == None:
            has_subtitle = DurhamHoldParser.has_subtitle(data_to_parse)

        if has_subtitle:
            item_date = data_to_parse[self.parse_rule.item_date_with_subtitle]
        else:
            item_date = data_to_parse[self.parse_rule.item_date_without_subtitle]
        
        item_date = item_date.replace("Due by ", "")
        
        return item_date

    def all(self, data_to_parse, generic_format, has_subtitle=None):
        if not(has_subtitle):
            has_subtitle = DurhamCheckoutParser.has_subtitle(data_to_parse)
        return [
            self.title(data_to_parse),
            self.format(data_to_parse),
            self.contributors(data_to_parse, generic_format, has_subtitle),
            self.status(data_to_parse,has_subtitle),
            self.item_date(data_to_parse, has_subtitle)
        ]

