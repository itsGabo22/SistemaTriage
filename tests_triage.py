import unittest
from src.models.hospital import Hospital
from src.models.patient import Patient

# Map the structure to the requested User Snippet
TriageSystem = Hospital

class TestTriageFlow(unittest.TestCase):
    def test_icu_overflow(self):
        # The code is in English
        system = TriageSystem(num_uci_beds=15)
        
        # Fill the ICU Array
        for i in range(15):
            mock_patient = Patient(id=f"P_{i}", name=f"Name_{i}", triage_lvl=3)
            system.assign_bed(mock_patient)
            
        self.assertTrue(system.is_icu_full())
        
        # New critical patient arrives
        critical_patient = Patient(id="P_CRITICO", name="Critico", triage_lvl=1)
        result_message = system.process_arrival(critical_patient)
        
        # The assertion checks for the SPANISH message that the Streamlit UI will display
        self.assertEqual(result_message, "Alerta: UCI Llena. Iniciando protocolo de desbordamiento.")

    def test_undo_stack_collision(self):
        system = TriageSystem(num_uci_beds=15)
        
        # Setup for the collision test 
        patient_a = Patient(id="Patient_A", name="A", triage_lvl=2)
        system.assign_bed(patient_a) # Occupies Bed 0
        
        # Discharge Patient A
        system.discharge_patient(0) # Bed 0 is now empty, action is pushed to stack
        
        # New patient occupies bed 0 directly (force collision without adding to undo stack)
        patient_b = Patient(id="Patient_B", name="B", triage_lvl=1)
        system.uci_beds[0] = patient_b
        
        # Try to undo the discharge! Oh no, the bed is occupied.
        undo_result = system.undo_last_action()
        
        # The code logic evaluates the collision, but the user sees the Spanish warning
        current_bed = system.get_bed(0)
        self.assertIsNotNone(current_bed)
        self.assertEqual(current_bed.patient.id, "Patient_B")
        self.assertEqual(undo_result, "Error: No se puede deshacer el alta. La cama ya está ocupada por un nuevo paciente.")

if __name__ == '__main__':
    unittest.main()
