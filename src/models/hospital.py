from src.data_structures.queue import Queue
from src.data_structures.stack import Stack
from src.models.patient import Patient

class Hospital:
    """Manager class for hospital state."""
    def __init__(self, num_uci_beds=15):
        # Arrays: Using a list with fixed size to simulate an array for UCI beds
        self.uci_beds = [None] * num_uci_beds
        
        # Queues: For priority 4 and 5 patients
        self.waiting_room = Queue()
        
        # Stacks: For Undo system
        self.undo_stack = Stack()
        
        # Native Lists: For medical staff
        self.medical_staff = []
        
        # Registry of all patients
        self.all_patients = {}

    def register_patient(self, id, name, triage_lvl):
        patient = Patient(id, name, triage_lvl)
        self.all_patients[id] = patient
        
        # Logic: Priority 1-3 usually go to intensive areas or immediate care (simplified)
        # Priority 4-5 go to the waiting room queue
        if triage_lvl >= 4:
            self.waiting_room.enqueue(patient)
            self.undo_stack.push({"action": "register", "patient_id": id, "target": "waiting_room"})
        else:
            # For simplicity, assign to UCI if Triage 1 or 2 and beds available
            self.assign_to_uci(patient)
        
        return patient

    def assign_to_uci(self, patient):
        for i in range(len(self.uci_beds)):
            if self.uci_beds[i] is None:
                self.uci_beds[i] = patient
                patient.status = "In Bed (UCI)"
                self.undo_stack.push({"action": "assign_uci", "patient_id": patient.id, "bed_index": i})
                return True
        return False

    def add_doctor(self, doctor):
        self.medical_staff.append(doctor)

    def undo_last_action(self):
        action = self.undo_stack.pop()
        if not action:
            return None
        
        # Basic undo logic
        if action["action"] == "register":
            p_id = action["patient_id"]
            if action["target"] == "waiting_room":
                # This is tricky with queues if they're already moved, 
                # but for initial structure, we'll keep it simple.
                pass 
            self.all_patients.pop(p_id, None)
        elif action["action"] == "assign_uci":
            bed_idx = action["bed_index"]
            p_id = action["patient_id"]
            self.uci_beds[bed_idx] = None
            patient = self.all_patients.get(p_id)
            if patient:
                patient.status = "Waiting"
        
        return action
