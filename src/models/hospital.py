import json
import os
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

    def assign_bed(self, patient):
        """English alias for assign_to_uci to satisfy test suite."""
        return self.assign_to_uci(patient)

    def is_icu_full(self):
        """Check if all beds in the ICU are occupied."""
        return all(bed is not None for bed in self.uci_beds)

    def get_bed(self, index):
        """Retrieve a patient from a specific bed index."""
        if 0 <= index < len(self.uci_beds):
            return self.uci_beds[index]
        return None

    def discharge_patient(self, bed_index):
        """Release a bed and set patient status to Discharged."""
        if 0 <= bed_index < len(self.uci_beds):
            patient = self.uci_beds[bed_index]
            if patient:
                patient.status = "Discharged"
                self.uci_beds[bed_index] = None
                # Save patient state for undo
                self.undo_stack.push({"action": "discharge", "patient": patient, "bed_index": bed_index})
                # Check if someone from waiting room can take the bed
                self.process_waiting_room()
                return True
        return False

    def process_waiting_room(self):
        """Check if beds are available for patients in the waiting room."""
        if not self.waiting_room.is_empty():
            # Find first empty bed
            for i in range(len(self.uci_beds)):
                if self.uci_beds[i] is None:
                    next_patient = self.waiting_room.dequeue()
                    if next_patient:
                        self.uci_beds[i] = next_patient
                        next_patient.status = "In Bed (UCI)"
                        self.undo_stack.push({"action": "auto_assign", "patient_id": next_patient.id, "bed_index": i})
                        # Recursively process if more beds/patients exist
                        self.process_waiting_room()
                        break

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

    def save_to_file(self, filename="hospital_data.json"):
        """Save current hospital state to a JSON file."""
        data = {
            "num_uci_beds": len(self.uci_beds),
            "all_patients": [
                {
                    "id": getattr(p, 'id', 'unknown'),
                    "name": getattr(p, 'name', 'unknown'),
                    "triage_lvl": getattr(p, 'triage_lvl', 5),
                    "status": getattr(p, 'status', 'unknown'),
                    "history": p.history.to_list() if hasattr(p, 'history') else []
                } for p in self.all_patients.values() if p is not None
            ],
            # We don't save medical_staff for brevity, but could be added
            "uci_beds_ids": [p.id if p else None for p in self.uci_beds],
            "waiting_room_ids": [p.id for p in self.waiting_room.to_list()]
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        return True

    @classmethod
    def load_from_file(cls, filename="hospital_data.json"):
        """Load hospital state from a JSON file."""
        if not os.path.exists(filename):
            return None
            
        with open(filename, 'r') as f:
            data = json.load(f)
            
        hospital = cls(data["num_uci_beds"])
        
        # Restore all patients
        for p_data in data["all_patients"]:
            p = Patient(p_data["id"], p_data["name"], p_data["triage_lvl"])
            p.status = p_data["status"]
            for h_item in p_data["history"]:
                p.add_intervention(h_item)
            hospital.all_patients[p.id] = p
            
        # Restore UCI beds
        for i, p_id in enumerate(data["uci_beds_ids"]):
            if p_id:
                hospital.uci_beds[i] = hospital.all_patients.get(p_id)
                
        # Restore Waiting Room
        for p_id in data["waiting_room_ids"]:
            p = hospital.all_patients.get(p_id)
            if p:
                hospital.waiting_room.enqueue(p)
                
        return hospital
