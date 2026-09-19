from __future__ import annotations
from typing import Any
from .node import Node

class PriorityNode(Node):
    next: PriorityNode | None # a PriorityNode only links to other PriorityNodes

    def __init__(self, data: Any, priority: float, next: PriorityNode | None = None):
        super().__init__(data, next)
        self.priority = priority