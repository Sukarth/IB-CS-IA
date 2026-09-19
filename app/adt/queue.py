from typing import Any
from .linked_list import LinkedList
from .node import Node

class Queue:
    def __init__(self):
        self._list = LinkedList()

    def enqueue(self, item: Any):
        """Add an element to the end of the queue."""
        self._list.append(Node(item))
        return self

    def dequeue(self):
        """Remove first element of the queue and return resulting first element."""
        return self._list.pop()

    def peek(self):
        """Return the element at the front of the queue without removing it."""
        if self._list.head is None:
            raise IndexError("Cannot peek at an empty queue")
        return self._list.head.data

    def is_empty(self):
        """Check if the queue is empty."""
        return self._list.count == 0

    def size(self):
        """Return the number of elements in the queue."""
        return self._list.count