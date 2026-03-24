# Sistema de Triage y Flujo de Sala de Urgencias 🏥

Proyecto base modularizado para la clase de **Estructuras de Datos**. 

## 📋 Requisitos Implementados

1.  **Arreglos (Arrays)**: Representación de 15 camas UCI en `Hospital.uci_beds`. Acceso por índice.
2.  **Colas (Queues)**: Gestión de sala de espera general (Pacientes Triage 4 y 5) en `src/data_structures/queue.py`.
3.  **Pilas (Stacks)**: Sistema de "Deshacer" (Undo) para revertir registros o asignaciones en `src/data_structures/stack.py`.
4.  **Listas Nativas**: Directorio de personal médico dinámico en `Hospital.medical_staff`.
5.  **Listas Simples (Singly Linked Lists)**: Historial de intervenciones por paciente en `src/data_structures/linked_list.py`.

## 🚀 Cómo Ejecutar

1.  Asegúrate de tener Python instalado.
2.  Crea un entorno virtual (opcional pero recomendado):
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```
3.  Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```
4.  Ejecuta la aplicación:
    ```bash
    streamlit run app.py
    ```

## 👥 División de Tareas (Roadmap)

Para completar este proyecto, el equipo se ha dividido las responsabilidades de la siguiente manera:

### 🛠️ Gabo (Gabriel) - Arquitectura & Backend
- Optimización de las estructuras de datos (`src/data_structures`).
- Lógica central de gestión hospitalaria en `Hospital.py`.
- Implementación de persistencia de datos (si se requiere).

### 🎨 Caliche - Diseño, UX/UI & Visualización Data
- **Estilo Pro**: Implementar un modo oscuro/claro y mejorar el CSS de las "tarjetas" de paciente.
- **Gráficos en Tiempo Real**: Usar Plotly para mostrar la ocupación de camas y tiempos de espera.
- **Dashboard Médico**: Crear una vista de "Monitor de Signos Vitales" (simulado) para pacientes en UCI.

### 🧪 Cristian - Datos, Inteligencia & Reportes
- **Simulador de Emergencias**: Crear un botón que genere 10 pacientes aleatorios para probar la cola.
- **Reportes PDF/CSV**: Implementar la descarga del historial médico del paciente.
- **Lógica de Triage**: Crear un asistente que sugiera el nivel de triage basado en síntomas (Ej: "Dolor pecho" -> P1).
- **Análisis de Datos**: Calcular estadísticas de eficiencia hospitalaria (Ej: tiempo promedio en espera).

## 🤝 Colaboración y Git (Cómo no pisarse el código)

Para trabajar los 3 al tiempo sin conflictos, sigan estas reglas:

1. **Uso de Ramas (Branches)**: No suban nada directamente a `main`. Cada uno trabaje en su rama:
   - `git checkout -b feature-backend-gabo`
   - `git checkout -b feature-ui-caliche`
   - `git checkout -b feature-tests-cristian`
2. **Modularidad**:
   - **Gabo**: Solo toca archivos dentro de `src/data_structures` y `src/models/hospital.py`.
   - **Caliche**: Solo toca `app.py` y archivos de estilo.
   - **Cristian**: Crea archivos nuevos en una carpeta `tests/`.
3. **Pull Requests**: Cuando terminen una mejora, suban su rama y hagan un "Pull Request".
4. **Fusión Segura (Safe Merge)**: Si alguien más ya unió cambios a `main`:
   - Primero: `git checkout main` y `git pull origin main`.
   - Segundo: Vuelve a tu rama: `git checkout mi-rama`.
   - Tercero: Une los cambios de main a tu rama: `git merge main`.
   - Cuarto: Resuelve conflictos si los hay (¡aquí es donde Antigravity les ayuda!) y luego sube tu rama.

## 🐛 Errores Conocidos y Soluciones

1.  **Errores de Importación**: Se han añadido archivos `__init__.py` para que Python reconozca `src` como un paquete modular.
2.  **Type Hints**: Se agregaron anotaciones de tipo en `linked_list.py` para evitar advertencias de "NoneType" en el análisis estático.
3.  **Ambiente Virtual**: Asegúrate de activar tu entorno virtual antes de ejecutar para que Streamlit sea detectado correctamente.
