import random
from datetime import datetime
from typing import TypedDict, List, Any
try:
    from faker import Faker      # type: ignore
    fake: Any = Faker('es_CO')   # type: ignore
except ImportError:
    # Error shown to the user if they try to run the script manually
    raise ImportError("Falta la librería Faker. Ejecuta: pip install faker")

class MockPatient(TypedDict):
    id: str
    name: str
    age: int
    main_symptom: str
    triage_level: int
    arrival_time: datetime

# 1.1 Define clinical rules (User-facing values stay in Spanish)
triage_symptoms = {
    # Level 1: Resuscitation (Immediate attention)
    1: ["Paro cardíaco", "Dificultad respiratoria severa", "Hemorragia masiva"],
    
    # Level 2: Emergency (< 15 min)
    2: ["Dolor en el pecho crónico", "Sospecha de ACV", "Quemadura grave", "Caída libre"],
    
    # Level 3: Urgency (< 60 min)
    3: ["Fractura expuesta", "Dolor abdominal fuerte", "Corte profundo", "Caída libre"],
    
    # Level 4: Minor Priority (< 120 min)
    4: ["Fiebre alta", "Esguince", "Vómito leve", "Caída libre"],
    
    # Level 5: Non-Urgent (< 240 min)
    5: ["Resfriado común", "Dolor de garganta", "Renovación de receta"]
}

# 1.2 Generate realistic distribution
def generate_mock_patients(amount: int) -> List[MockPatient]:
    patients: List[MockPatient] = []
    
    # Define weights: Level 1 (2%), Level 2 (8%), Level 3 (30%), Level 4 (40%), Level 5 (20%)
    levels = [1, 2, 3, 4, 5]
    probabilities = [0.02, 0.08, 0.30, 0.40, 0.20]
    
    nn_counter: int = 0
    
    for _ in range(amount):
        assigned_level = int(random.choices(levels, weights=probabilities, k=1)[0])
        symptom = str(random.choice(triage_symptoms[assigned_level]))
        age = int(random.randint(1, 95))
        
        # 1.3 Edge Cases
        # Decreasing priority level number means increasing priority (e.g., from 3 to 2)
        if age > 80 and symptom == "Caída libre":
            if assigned_level > 1:
                assigned_level = assigned_level - 1
        
        # 1% of patients without registered name (NN)
        patient_name: str = ""
        if random.random() < 0.01:
            nn_counter += 1  # type: ignore
            # User facing, keep in Spanish
            patient_name = f"Paciente NN_{nn_counter:03d}"
        else:
            patient_name = str(fake.name()) # type: ignore
            
        _id: str = str(fake.uuid4()) # type: ignore
        
        patient: MockPatient = {
            "id": _id[:8], # type: ignore
            "name": patient_name,
            "age": age,
            "main_symptom": symptom,
            "triage_level": assigned_level,
            "arrival_time": fake.date_time_between(start_date="-1d", end_date="now") # type: ignore
        }
        patients.append(patient)
        
    return patients

if __name__ == "__main__":
    # Generate 100 test patients
    mock_data = generate_mock_patients(100)
    
    print(f"Generados {len(mock_data)} pacientes.") # User facing output in Spanish
    
    # Show some example patients, paying attention to NNs or Edge Cases if they exist
    nns = [p for p in mock_data if str(p.get("name", "")).startswith("Paciente NN")]
    fails = [p for p in mock_data if p.get("main_symptom") == "Caída libre" and int(p.get("age", 0)) > 80] # type: ignore
    
    print("\nEjemplo de pacientes generados:") # User facing output in Spanish
    
    # To avoid typed dict slice pyright error:
    count = 0
    for p in mock_data:
        if count >= 3:
            break
        print(p)
        count += 1
        
    print(f"\nPacientes NN generados: {len(nns)}") # User facing output in Spanish
    if nns:
        print("Ejemplo NN:", nns[0])
        
    print(f"Pacientes > 80 con Caída Libre generados: {len(fails)}") # User facing output in Spanish
    if fails:
        print("Ejemplo Caída libre (>80):", fails[0])
