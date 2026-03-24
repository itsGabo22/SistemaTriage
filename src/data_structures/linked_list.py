from typing import Optional

class Node:
    """A node in a singly linked list."""
    def __init__(self, data=None):
        self.data = data
        self.next: Optional[Node] = None

class SinglyLinkedList:
    """Custom implementation of a Singly Linked List for intervention history."""
    def __init__(self):
        self.head: Optional[Node] = None
        self.size = 0

    def append(self, data):
        """Add a new node at the end of the list."""
        new_node = Node(data)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            # Satisfy linter that current is not None (head was checked above)
            while current is not None and current.next is not None:
                current = current.next
            if current is not None:
                current.next = new_node
        self.size += 1

    def delete(self, data):
        """Remove the first occurrence of data in the list."""
        if self.head is None:
            return False
        
        if self.head.data == data:
            self.head = self.head.next
            self.size -= 1
            return True
            
        current = self.head
        while current is not None:
            # Check current.next explicitly
            next_node = current.next
            if next_node is not None:
                if next_node.data == data:
                    current.next = next_node.next
                    self.size -= 1
                    return True
            current = next_node
        return False

    def to_list(self):
        """Convert the linked list to a Python list for easier display."""
        items = []
        current = self.head
        while current is not None:
            items.append(current.data)
            current = current.next
        return items

    def __iter__(self):
        current = self.head
        while current:
            yield current.data
            current = current.next

    def __len__(self):
        return self.size
