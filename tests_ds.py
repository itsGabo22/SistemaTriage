from src.data_structures.linked_list import SinglyLinkedList
from src.data_structures.stack import Stack
from src.data_structures.queue import Queue

def test_linked_list():
    ll = SinglyLinkedList()
    ll.append("Step 1")
    ll.append("Step 2")
    assert ll.to_list() == ["Step 1", "Step 2"]
    assert len(ll) == 2
    print("SinglyLinkedList: OK")

def test_stack():
    s = Stack()
    s.push("Action 1")
    s.push("Action 2")
    assert s.pop() == "Action 2"
    assert s.peek() == "Action 1"
    assert s.size() == 1
    print("Stack: OK")

def test_queue():
    q = Queue()
    q.enqueue("Patient A")
    q.enqueue("Patient B")
    assert q.dequeue() == "Patient A"
    assert q.size() == 1
    print("Queue: OK")

if __name__ == "__main__":
    test_linked_list()
    test_stack()
    test_queue()
    print("All custom data structures verified!")
