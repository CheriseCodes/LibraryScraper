class Library():
    def __init__(self, name) -> None:
        self._hours = []
        self._items = []
        self._name = name
    
    def get_hours_str(self):
        ret = ""
        for day in self._hours:
            ret += day + '\n'
        return ret

    def get_items_str(self):
        return self._items
