"""Module for the superclass container as well as its two subclasses Stack and Queue"""


class Container:
    """Superclass for """

    def __init__(self, items):
        if items is None:
            self.items = []
        else:
            self.items = items

    def size(self):
        """Return the number of elements"""
        return len(self.items)

    def is_empty(self):
        """Return true if container is empty"""
        return len(self.items) == 0

    def push(self, item):
        """Push new item to end of container"""
        self.items.append(item)

    def pop(self):
        """Pop item, must be overriden by subclasses"""
        raise NotImplementedError

    def peek(self):
        """Peek top item, must be overriden by subclasses"""
        raise NotImplementedError

    def __str__(self):
        as_string = ""
        for item in self.items:
            as_string += " " + str(item)

        return as_string


class Queue(Container):
    """LIFO implementation of Container"""

    def __init__(self, items=None):
        super().__init__(items)

    def peek(self):
        """Retun first item if it exists"""
        assert not self.is_empty()
        return self.items[0]

    def pop(self):
        """Pop first item"""
        assert not self.is_empty()
        return self.items.pop(0)


class Stack(Container):
    """Fifo implementation of Container"""

    def __init__(self, items=None):
        super().__init__(items)

    def peek(self):
        """Retun last item if it exists"""
        assert not self.is_empty()
        return self.items[-1]

    def pop(self):
        """Pop last item"""
        assert not self.is_empty()
        item = self.items.pop()
        return item
