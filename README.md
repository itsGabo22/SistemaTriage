# 🏥 Sistema de Triage y Flujo de Urgencias - Hospital v1.0

Este proyecto es una simulación avanzada de un centro de triage de urgencias, desarrollado para el taller de **Estructuras de Datos**. Integra una interfaz premium con un motor de backend robusto y análisis de datos optimizado.

---

## 🛠️ Requisitos e Instalación

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/itsGabo22/SistemaTriage.git
   cd SistemaTriage
   ```

2. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecutar la aplicación**:
   ```bash
   streamlit run app.py
   ```

---

## 🧠 Estructuras de Datos Implementadas

El proyecto cumple con los requisitos académicos mediante el uso estratégico de diversas estructuras de datos:

### 1. 🗂️ Arrays (Listas de Acceso Fijo)
- **Uso**: Implementado en la gestión de las **15 Camas UCI**.
- **Por qué**: Permite acceso aleatorio $O(1)$ a cualquier cama específica para dar el alta o asignar un paciente basado en disponibilidad inmediata.

### 2. ⏳ Colas (Queues - FIFO)
- **Uso**: Gestiona la **Sala de Espera General** para pacientes con Triage 4 y 5.
- **Por qué**: Garantiza la justicia en la atención, donde el primer paciente en llegar es el primero en ser atendido (First-In, First-Out).

### 3. ↩️ Pilas (Stacks - LIFO)
- **Uso**: Motor del sistema **Undo (Deshacer)**.
- **Por qué**: Almacena el historial de acciones (registros, altas) permitiendo revertir la última operación realizada, siguiendo el principio Last-In, First-Out.

### 4. 📜 Listas Simplemente Enlazadas (Singly Linked Lists)
- **Uso**: Almacena el **Historial de Intervenciones** de cada paciente.
- **Por qué**: Permite añadir registros médicos de forma dinámica sin necesidad de redimensionar memoria, manteniendo la cronología de la atención.

### 5. 🔍 Hash-Maps (Diccionarios de Python)
- **Uso**: Utilizado en el módulo de **Analytics/Reportes**.
- **Por qué**: Ofrece una búsqueda de pacientes por intervención en tiempo constante $O(1)$, optimizando el rendimiento de la aplicación incluso con grandes volúmenes de datos.

---

## 👨‍💻 Equipo de Desarrollo
- **Gabo (itsGabo22)**: Lógica Core, Estructuras de Datos y Persistencia.
- **Caliche**: Diseño UI/UX Premium, Animaciones CSS y Gráficos Plotly.
- **Cristian**: Generador de Datos (Mock), Analítica O(1) y Testing.

---

## 🧪 Pruebas Unitarias
El sistema incluye una suite de pruebas para validar la integridad de las estructuras:
- `python tests_triage.py`: Valida el flujo de urgencias y colisiones de Undo.
- `python tests_ds.py`: Valida el funcionamiento técnico de las estructuras personalizadas.

---
*Desarrollado para el taller de Estructuras de Datos - 2024*
