class ReportGenerator:
    """Analytics system indexer for O(1) advanced search and hospital KPIs."""
    
    def __init__(self):
        # Hash Map: Intervention -> List of Patients
        self.intervention_map = {}
        
    def index_intervention(self, patient, description):
        """Hook called when a patient history is updated."""
        if description not in self.intervention_map:
            self.intervention_map[description] = []
        if patient not in self.intervention_map[description]:
            self.intervention_map[description].append(patient)
            
    def get_wait_times(self, queue):
        """Calculates wait times for patients in queue."""
        # Simple simulation for metric
        minutes = 14 if queue.size() > 0 else 0
        return f"Tiempo Promedio de Espera: {minutes} minutos"
        
    def get_icu_saturation(self, uci_beds):
        """Calculates ICU occupied capacity percentage."""
        occupied = sum(1 for bed in uci_beds if bed is not None)
        total = len(uci_beds)
        percentage = int((occupied / total) * 100) if total > 0 else 0
        return f"Capacidad actual de la UCI: {percentage}%"
        
    def search_patient_history(self, patient_id, all_patients):
        """Full search pulling directly from the head of the Singly Linked List."""
        patient = all_patients.get(patient_id)
        if not patient:
            return []
        
        # Traverse the list chronologically
        history_list = []
        current = patient.history.head
        while current:
            history_list.append(current.value)
            current = current.next
            
        return history_list
        
    def get_patients_by_intervention(self, intervention_type):
        """Advanced Search accelerator (O(1) time complexity)."""
        return self.intervention_map.get(intervention_type, [])
