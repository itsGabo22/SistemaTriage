class Doctor:
    """Represents a medical staff member."""
    def __init__(self, id, name, specialty):
        self.id = id
        self.name = name
        self.specialty = specialty

    def __repr__(self):
        return f"Dr. {self.name} ({self.specialty})"
