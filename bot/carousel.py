class Carousel(object):
    def __init__(self):
        self.__items = []
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

    def set_items(self, items):
        self.__items = items
        self.__current_index = 0

    def next(self):
        try:
            current_item = self.__items[self.__current_index + 1]
            self.__current_index += 1
            return current_item
        except IndexError as e:
            self.__current_index = 0
            print(e)
        return None

    def previous(self):
        try:
            current_item = self.__items[self.__current_index - 1]
            self.__current_index -= 1
            if self.__current_index == -1:
                self.__current_index = len(self.__items) - 1
            return current_item
        except IndexError as e:
            self.__current_index = 0
            print(e)
        return None
