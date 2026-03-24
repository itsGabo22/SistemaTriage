from src.data_structures.linked_list import SinglyLinkedList

class Patient:
    """Represents a patient in the ER."""
    def __init__(self, id, name, triage_lvl):
        self.id = id
        self.name = name
        self.triage_lvl = triage_lvl  # 1 (Emergency) to 5 (Non-urgent)
        self.history = SinglyLinkedList()
        self.status = "Waiting" # Waiting, In Bed, Discharged

    def add_intervention(self, description):
        """Add a medical procedure to the patient's history."""
        self.history.append(description)

    def __repr__(self):
        return f"Patient({self.id}, {self.name}, Triage: {self.triage_lvl})"
