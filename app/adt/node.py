from __future__ import annotations
from typing import Any

class Node:
    def __init__(self, data: Any, next: Node | None = None):
        self.data = data
        self.next = next
