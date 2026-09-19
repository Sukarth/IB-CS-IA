from typing import Any
from .linked_list import LinkedList
from .priority_node import PriorityNode

class PriorityQueue:
    def __init__(self):
        self._list = LinkedList()

    def enqueue(self, item: Any, priority: float):
        """Add an element to the queue based on its priority."""
        new_node = PriorityNode(item, priority)
        if not self._list.head or self._list.head.priority < priority:
           self._list.prepend(new_node)
        else:
            current = self._list.head
            while current.next and current.next.priority >= priority:
                current = current.next
            new_node.next = current.next
            current.next = new_node
            if new_node.next is None:
                self._list.tail = new_node
        self._list.count += 1

    def dequeue(self):
        """Remove the highest priority element from the queue."""
        if not self._list.head or self.is_empty():
            raise IndexError("Cannot dequeue from an empty queue")
        return self._list.delete(self._list.head.data).head.data

    def peek(self):
        """Return the highest priority element without removing it."""
        if not self._list.head or self.is_empty():
            raise IndexError("Cannot peek at an empty queue")
        return self._list.head.data

    def is_empty(self):
        """Check if the queue is empty."""
        return self._list.count == 0

    def size(self):
        """Return the number of elements in the queue."""
        return self._list.count    