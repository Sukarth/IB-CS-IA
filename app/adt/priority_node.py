from __future__ import annotations
from typing import Any
from .node import Node

class PriorityNode(Node):
    def __init__(self, data: Any, priority: float, next: Node | None = None):
        super().__init__(data, next)
        self.priority = priority