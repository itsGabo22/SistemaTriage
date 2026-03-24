import unittest
from src.models.hospital import Hospital
from src.models.patient import Patient

# Map the structure to the requested User Snippet
TriageSystem = Hospital

class TestTriageFlow(unittest.TestCase):
    def test_icu_overflow(self):
        system = TriageSystem(num_uci_beds=15)
        
        # Fill the ICU Array
        for i in range(15):
            mock_p = Patient(id=f"P_{i}", name=f"Name_{i}", triage_lvl=3)
            system.assign_bed(mock_p)
            
        self.assertTrue(system.is_icu_full())
        
        # New critical patient arrives
        crit_p = Patient(id="P_CRITICO", name="Critico", triage_lvl=1)
        system.register_patient(crit_p.id, crit_p.name, crit_p.triage_lvl)
        
        # Verify overflow (the patient should NOT be in a bed)
        self.assertTrue(system.is_icu_full())
        self.assertNotIn(crit_p, system.uci_beds)

    def test_undo_stack_collision(self):
        system = TriageSystem(num_uci_beds=15)
        
        # Setup for the collision test 
        p_a = Patient(id="Patient_A", name="A", triage_lvl=2)
        system.assign_bed(p_a) # Occupies Bed 0
        
        # Discharge Patient A
        system.discharge_patient(0) # Bed 0 is now empty, action is pushed to stack
        
        # New patient occupies bed 0 directly (force collision)
        p_b = Patient(id="Patient_B", name="B", triage_lvl=1)
        system.uci_beds[0] = p_b
        
        # Action is returned by undo_last_action
        undo_result = system.undo_last_action()
        self.assertIsNotNone(undo_result)
        
        # Current bed is still occupied by Patient B
        current_p = system.get_bed(0)
        self.assertEqual(current_p.id, "Patient_B")

if __name__ == '__main__':
    unittest.main()
