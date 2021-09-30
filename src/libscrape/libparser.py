from abc import ABC, abstractmethod

# NOTE: ParserRule is just a dictionary that maps each expected piece of data
# to an index


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

class DurhamHoldParser(LibraryParser):
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

    def title(self, data_to_parse):
        return data_to_parse[self.parse_rule["title"]].rsplit(", ",1)[0]

    def format(self, data_to_parse):
        return data_to_parse[self.parse_rule["format"]].rsplit(", ",1)[1]

    @staticmethod
    def format(data_to_parse):
        return data_to_parse[2].rsplit(", ",1)[1]

    @staticmethod
    def title(data_to_parse):
        return data_to_parse[2].rsplit(", ",1)[0]

    def contributors(self, data_to_parse, has_subtitle=None):

        if has_subtitle == None:
            has_subtitle = DurhamHoldParser.has_subtitle(data_to_parse)
       
        if has_subtitle:
            return data_to_parse[self.parse_rule["contributors_with_subtitle"]]
        else:
            return data_to_parse[self.parse_rule["contributors_without_subtitle"]]

    def status(self, data_to_parse, has_subtitle=None):
        if has_subtitle == None:
            has_subtitle = DurhamHoldParser.has_subtitle(data_to_parse)

        if has_subtitle:
            status = data_to_parse[self.parse_rule["status_with_subtitle"]]
        else:
            status = data_to_parse[self.parse_rule["status_without_subtitle"]]

        if "Not ready" in status:
            return "Not Ready"
        else:
            return "Ready"

    def item_date(self, data_to_parse, has_subtitle=None):
        if has_subtitle == None:
            has_subtitle = DurhamHoldParser.has_subtitle(data_to_parse)

        if has_subtitle:
            item_date = data_to_parse[self.parse_rule["item_date_with_subtitle"]]
        else:
            item_date = data_to_parse[self.parse_rule["item_date_without_subtitle"]]
        
        if "Expires on " in item_date:
            item_date = item_date.replace("Expires on ", "")
        elif "Pick up by " in item_date:
            item_date = item_date.replace("Pick up by", "")
        
        return item_date

    def branch(self, data_to_parse, has_subtitle=None):
        if has_subtitle == None:
            has_subtitle = DurhamHoldParser.has_subtitle(data_to_parse)
        
        if has_subtitle:
            branch = data_to_parse[self.parse_rule["branch_with_subtitle"]]
        else:
            branch = data_to_parse[self.parse_rule["branch_without_subtitle"]]
        
        return branch.replace("Pick up by ", "")

    def all(self, data_to_parse):
        return [self.title(data_to_parse), self.format(data_to_parse), self.contributors(data_to_parse), self.status(data_to_parse)]


