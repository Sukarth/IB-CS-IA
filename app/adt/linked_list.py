from .node import Node
from typing import Any

class LinkedList:
    def __init__(self, head: Node | None = None, tail: Node | None = None, count: int = 0):
        self.head = head
        self.tail = tail
        self.count = count

    def append(self, node: Node):
        if not self.head:
            self.head = node
            self.tail = node
        if self.tail:
            self.tail.next = node
            self.tail = node
        self.count += 1
        return self

    def prepend(self, node: Node):
        node.next = self.head
        self.head = node
        if not self.tail:
            self.tail = node
        self.count += 1
        return self


    def delete(self, key: Any):
        # 1. Empty list check
        if not self.head:
            raise ValueError(f"Node with data {key} not found.")
        
        # 2. Handle deleting the head
        if self.head.data == key:
            if self.head == self.tail:
                self.tail = None  # List becomes empty
            self.head = self.head.next
            self.count -= 1
            return self
        
        # 3. Handle deleting middle or tail nodes
        curr = self.head
        while curr.next:
            if curr.next.data == key:
                if curr.next == self.tail:
                    self.tail = curr  # Update tail if last node is being deleted
                curr.next = curr.next.next  # Unlink target node
                self.count -= 1
                return self
            curr = curr.next
        
        raise ValueError(f"Node with data {key} not found.")

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