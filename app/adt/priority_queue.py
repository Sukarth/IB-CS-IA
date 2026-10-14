from typing import Any
from .priority_linked_list import PriorityLinkedList
from .priority_node import PriorityNode

class PriorityQueue:
    def __init__(self):
        self._list = PriorityLinkedList()

    def enqueue(self, item: Any, priority: float):
        """Add an element to the queue based on its priority."""
        self._list.insert_in_order(PriorityNode(item, priority))
        return self

    def dequeue(self):
        """Remove and return the highest priority element from the queue."""
        return self._list.pop()

    def peek(self):
        """Return the highest priority element without removing it."""
        if self._list.head is None:
            raise IndexError("Cannot peek at an empty queue")
        return self._list.head.data

    def is_empty(self):
        """Check if the queue is empty."""
        return self._list.count == 0

    def size(self):
        """Return the number of elements in the queue."""
        return self._list.count    