class Carousel(object):
    """Control that scrolls through all items like carousel
    if end is reached starts from the beginning"""

    def __init__(self, name=None):
        self.name = name
        self.__items = []
        self.__current_index = 0

    def set_items(self, items):
        self.__items = items
        self.__current_index = 0

    @property
    def current_index(self):
        return self.__current_index

    @property
    def total_items(self):
        return len(self.__items)

    @property
    def current_item(self):
        try:
            return self.__items[self.current_index]
        except IndexError as e:
            print(e)
        return None

    def next(self):
        try:
            current_item = self.__items[self.__current_index + 1]
            self.__current_index += 1
            return current_item
        except IndexError:
            self.__current_index = 0
            print('End has been reached')
            return self.current_item

    def previous(self):
        try:
            current_item = self.__items[self.__current_index - 1]
            self.__current_index -= 1
            if self.__current_index == -1:
                # if it stars scrolling backwards change index to index of the last element of the list
                self.__current_index = self.total_items - 1
            return current_item
        except IndexError:
            self.__current_index = 0
        return None
