from .node import Node
from typing import Any

class LinkedList:
    def __init__(self, head: Node | None = None, tail: Node | None = None, count: int = 0):
        self.head = head
        self.tail = tail
        self.count = count

    def append(self, node: Node):
        node.next = None
        if self.tail is None:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self.count += 1
        return self

    def prepend(self, node: Node):
        node.next = self.head
        self.head = node
        if self.tail is None:
            self.tail = node
        self.count += 1
        return self


    def delete(self, key: Any):
        # 1. Empty list check
        if self.head is None:
            raise ValueError(f"Node with data {key} not found.")
        
        # 2. Handle deleting the head
        if self.head.data == key:
            if self.head is self.tail:
                self.tail = None  # List becomes empty
            self.head = self.head.next
            self.count -= 1
            return self
        
        # 3. Handle deleting middle or tail nodes
        curr = self.head
        while curr.next:
            if curr.next.data == key:
                if curr.next is self.tail:
                    self.tail = curr  # Update tail if last node is being deleted
                curr.next = curr.next.next  # Unlink target node
                self.count -= 1
                return self
            curr = curr.next
        
        raise ValueError(f"Node with data {key} not found.")

    def pop(self):
        if self.head is None:
            raise IndexError("Cannot pop from an empty list.")
        
        popped_data = self.head.data
        if self.head is self.tail:
            self.head = None
            self.tail = None
        else:
            self.head = self.head.next
        
        self.count -= 1
        return popped_data

    def search(self, key: Any):
        current_node = self.head
        while current_node:
            if current_node.data == key:
                return True
            current_node = current_node.next
        return False

    def display(self):
        elements = []
        current_node = self.head
        while current_node:
            elements.append(current_node.data)
            current_node = current_node.next
        return elements