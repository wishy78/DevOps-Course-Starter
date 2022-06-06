class ViewModel:
    def __init__(self, items):
        self._items = items

    @property
    def items(self):
        return self._items

    @property
    def doing_items(self):
        doingItems = []
        for item in self.items:
            if item.status == "Doing":
                doingItems.append(item)
        return [doingItems]

    @property
    def toDo_items(self):
        toDoItems = []
        for item in self.items:
            if item.status == "To Do":
                toDoItems.append(item)
        return [toDoItems]

    @property
    def done_items(self):
        doneItems = []
        for item in self.items:
            if item.status == "Done":
                doneItems.append(item)
        return [doneItems]
