class FixedList(list):
    def __init__(self, length):
        super().__init__()
        self.length = length

    def append(self, item):
        list.append(self, item)
        if len(self) > self.length:
            del self[0]
