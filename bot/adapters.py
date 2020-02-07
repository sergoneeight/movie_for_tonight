class ResultsAdapter(object):
    def __init__(self, results):
        self._results = results
        self.__items = self.__gen()

    def __gen(self):
        chunk = []
        counter = 0
        for index, item in enumerate(self._results):
            counter += 1
            chunk.append(item)
            if counter == 19:
                counter = 0
                yield chunk
                chunk = []
            elif index == len(self._results) - 1:
                yield chunk

    def next_chunk(self):
        result = None
        try:
            result = next(self.__items)
        except StopIteration as e:
            print(e)
        return result
