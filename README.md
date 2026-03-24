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

### 🎨 Caliche - Diseño & UX/UI
- Estilo premium del Dashboard usando CSS custom.
- Mejora de la experiencia de usuario (gráficos, alertas, feedback visual).
- Responsividad de los paneles en Streamlit.

### 🧪 Cristian - Datos & Verificación
- Generación de datos de prueba (Mock Data).
- Implementación de pruebas integrales para el flujo de triage.
- Lógica de búsqueda avanzada y reportes históricos.

## 🐛 Errores Conocidos y Soluciones

1.  **Errores de Importación**: Se han añadido archivos `__init__.py` para que Python reconozca `src` como un paquete modular.
2.  **Type Hints**: Se agregaron anotaciones de tipo en `linked_list.py` para evitar advertencias de "NoneType" en el análisis estático.
3.  **Ambiente Virtual**: Asegúrate de activar tu entorno virtual antes de ejecutar para que Streamlit sea detectado correctamente.
