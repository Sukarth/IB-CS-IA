from .priority_node import PriorityNode
from .linked_list import LinkedList

class PriorityLinkedList(LinkedList):
    # a PriorityLinkedList only links to PriorityNodes
    head: PriorityNode | None
    tail: PriorityNode | None

    def insert_in_order(self, node: PriorityNode):
        """Insert a node into the linked list based on its priority."""
        if self.head is None or self.head.priority < node.priority:
            self.prepend(node)
        else:
            current = self.head
            while current.next and current.next.priority >= node.priority:
                current = current.next
            node.next = current.next
            current.next = node
            if node.next is None:
                self.tail = node
            self.count += 1
        return self