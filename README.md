# Gestor de Eventos de ACUSE.S.A.

Este proyecto fue desarrollado como parte del curso 2025-2026 de Programación en Ciencias de la Computación. 
Su objetivo es gestionar la planificación de eventos de una empresa, haciendo uso de recursos y respetando restricciones y reglas entre ellos.

---

## Dominio del proyecto

El dominio elegido es la **gestión de servicios de construcción, montaje, reparación y mantenimientos constructivos, tecnológicos y energéticos**. Esto incluye la organización de trabajos que requieren:

- Personal especializado.
- Materiales y equipos específicos.
- Vehículos o herramientas limitadas.

Se eligió este dominio porque permite practicar:

- Manejo de inventarios y recursos limitados.
- Validación de restricciones y reglas entre recursos más aplicadas a la realidad.
- Programación orientada a objetos y modular.
- Persistencia de datos mediante archivos JSON.
- Gestión de solapamientos de eventos y reprogramaciones automáticas.

---

## Eventos

Un **evento** representa una actividad planificada que requiere recursos y tiene una duración determinada. Cada evento tiene:

- **ID**: identificador único generado automáticamente.
- **Nombre**: tipo de evento, por ejemplo: "Instalación eléctrica en local".
- **Fecha de inicio y fin**.
- **Recursos requeridos**: cantidad de recursos humanos y materiales asignados.
- **Estado (`activated`)**:  
  - `False` si el evento es futuro.  
  - `True` si el evento está actualmente en ejecución (solo después de iniciar el programa en la fecha correspondiente).

### Tipos de eventos disponibles

| ID | Nombre del evento |
|----|-----------------|
| 1  | Instalación eléctrica en local |
| 2  | Mudanza con camión de carga |
| 3  | Construcción o reparación de inmueble |
| 4  | Mantenimiento de sistemas informáticos o de red |
| 5  | Montaje de domótica |
| 6  | Mantenimiento de fontanería |

---

## Recursos

### Recursos disponibles

| Recurso | Cantidad disponible |
|---------|------------------|
| Electricista | 3 |
| Plomero | 2 |
| Carpintero | 2 |
| Obrero | 5 |
| Operador de camión de carga | 2 |
| Técnico de redes | 3 |
| Técnico de domótica | 3 |
| Camión de carga | 2 |
| Sensores y dispositivos de domótica | 5 |
| Materiales de construcción | 5 |
| Kit de herramientas | 5 |
| Equipos de red | 5 |
| Accesorios de fontanería | 5 |
| Accesorios de electricidad | 5 |

### Restricciones entre recursos

1. **Inclusión obligatoria**: algunos recursos requieren otros para funcionar.  
   - Ejemplo: Si asignas un **Electricista**, se incluye automáticamente **Accesorios de electricidad**.
2. **Exclusión**: ciertos recursos no pueden coexistir en el mismo evento.  
   - Ejemplo: Un **Electricista** no puede trabajar junto a un **Plomero** en el mismo evento para evitar accidentes innecesarios.

> El sistema valida automáticamente estas reglas al crear eventos, incluyendo o bloqueando recursos según corresponda.

---

## Persistencia y activación de eventos

- Los eventos se guardan en el archivo `storage/eventos.json`.  
- Al iniciar el programa, los eventos futuros tienen `activated = False`.  
- Cuando llega la fecha de inicio de un evento y se ejecuta el programa, `activated` cambia a `True` hasta la finalización.  
- Los recursos se descuentan solo cuando el evento se activa, y se liberan cuando finaliza o se elimina un evento activo.

---

## Instalación y ejecución

### Requisitos

- Python 3.10 o superior.
- Entorno de desarrollo recomendado: VS Code, PyCharm o cualquier IDE compatible con Python.
- Asegurarse de que la carpeta `storage/` exista para guardar el JSON (`storage/eventos.json`).

### Clonar el proyecto

```bash
git clone https://github.com/Muzkatanke/planificador-inteligente-eventos.git
```

### Uso del programa

Al ejecutar main.py, se mostrará el menú principal:

#### Agregar evento:

- Selecciona el tipo de evento.
- Define fecha de inicio y fin.
- Asigna los recursos necesarios.
- El sistema validará restricciones, solapamientos y recursos disponibles, y sugerirá reprogramación automática si es necesario.

#### Eliminar evento:

- Selecciona un evento existente.
- Si estaba activo, los recursos se liberan automáticamente.

#### Ver eventos:
- Muestra todos los eventos cargados, con sus fechas y recursos asignados.

#### Salir:
- Cierra el programa.

---

### Estructura del código

- **Main.py**: punto de entrada; muestra menú y activa/desactiva eventos según fecha.

- **Datos.py**: define recursos y reglas de inclusión/exclusión.

- **Recursos.py**: valida automáticamente las reglas de inclusión y exclusión.

- **Evento.py**: define la clase `Event` y funciones auxiliares (`ask_date`, `find_available_start`, `available_amount`).

- **Planificador.py**: activa y desactiva eventos basándose en la fecha actual.

- **Manejo_Eventos.py**: funciones para agregar, eliminar y ver eventos.

- **Persistencia.py**: gestiona la lectura y escritura de eventos en JSON.
