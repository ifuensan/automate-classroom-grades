# Automate Github Classroom Grades Reports

## GitHub Classroom CLI

El plugin `gh-classroom` es una extensión para la herramienta de línea de comandos de GitHub (`gh`) que facilita la gestión de asignaciones y repositorios de estudiantes en GitHub Classroom. Con este plugin, puedes listar asignaciones, clonar repositorios de estudiantes, y obtener calificaciones de manera sencilla y eficiente.

### Instalación

Para instalar el plugin `gh-classroom`, ejecuta el siguiente comando:

```bash
gh extension install github/gh-classroom
```

Este comando descargará e instalará la extensión `gh-classroom` en tu entorno de `gh`, permitiéndote utilizar los comandos adicionales proporcionados por el plugin.

En este repositorio pretendo hacer un resumen de los comandos principales que luego usaré para el programa, pero [aquí](https://github.com/github/gh-classroom) se puede encontrar una explicación mucho más completa del plugin.

## Get assignments

```bash
gh classroom assignments
```

```bash
ID  Title  Submission Public  Type  Deadline  Editor  Invitation Link  Accepted  Submissions  Passing
```

### Grades

```bash
gh classroom assignment-grades
```

### Accepted assignments

El comando `gh classroom accepted-assignments` se utiliza para listar las asignaciones aceptadas en GitHub Classroom. Aquí hay una explicación detallada de cómo usar este comando:

```bash
gh classroom accepted-assignments
```

Este comando, sin ningún argumento adicional, mostrará una lista de todas las asignaciones aceptadas en tu GitHub Classroom.

#### Ejemplos de uso

Si deseas omitir el paso de selección y especificar directamente el ID de la asignación, puedes usar la opción `-a` seguida del ID de la asignación. Aquí hay dos ejemplos:

```bash
gh classroom accepted-assignments -a 605580 # accepted assignment id
gh classroom clone student-repos -a 612817 # student repo id
```

- **`gh classroom accepted-assignments -a 605580`**: Este comando lista las asignaciones aceptadas para la asignación con el ID `605580`.
- **`gh classroom clone student-repos -a 612817`**: Este comando clona los repositorios de los estudiantes para la asignación con el ID `612817`.

### Explicación del programa Python

A continuación, se explica el código fuente del programa Python de este proyecto. El fichero principal es `download-grades.py` y contiene las siguientes funciones:

```python
import requests

def get_accepted_assignments(api_url, assignment_id=None):
    url = f"{api_url}/accepted-assignments"
    if assignment_id:
        url += f"/{assignment_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching assignments: {response.status_code}")

def clone_student_repos(api_url, assignment_id):
    url = f"{api_url}/clone-repos/{assignment_id}"
    response = requests.post(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error cloning repos: {response.status_code}")

if __name__ == "__main__":
    api_url = "https://api.githubclassroom.com"
    assignment_id = 605580
    try:
        assignments = get_accepted_assignments(api_url, assignment_id)
        print("Accepted Assignments:", assignments)
        cloned_repos = clone_student_repos(api_url, assignment_id)
        print("Cloned Repositories:", cloned_repos)
    except Exception as e:
        print(e)
```

#### Explicación del código

1. **Importación de Módulos**:
    - `import requests`: Importa el módulo `requests` para realizar solicitudes HTTP.

2. **Función `get_accepted_assignments`**:
    - **Parámetros**:
        - `api_url`: La URL base de la API de GitHub Classroom.
        - `assignment_id`: (Opcional) El ID de la asignación.
    - **Descripción**:
        - Construye la URL para obtener las asignaciones aceptadas.
        - Realiza una solicitud GET a la API.
        - Si la respuesta es exitosa (código 200), devuelve los datos en formato JSON.
        - Si hay un error, lanza una excepción con el código de estado de la respuesta.

3. **Función `clone_student_repos`**:
    - **Parámetros**:
        - `api_url`: La URL base de la API de GitHub Classroom.
        - `assignment_id`: El ID de la asignación.
    - **Descripción**:
        - Construye la URL para clonar los repositorios de los estudiantes.
        - Realiza una solicitud POST a la API.
        - Si la respuesta es exitosa (código 200), devuelve los datos en formato JSON.
        - Si hay un error, lanza una excepción con el código de estado de la respuesta.

4. **Bloque Principal**:
    - Define la URL base de la API y el ID de la asignación.
    - Intenta obtener las asignaciones aceptadas y clonar los repositorios de los estudiantes.
    - Imprime los resultados o el error si ocurre una excepción.

Este código proporciona una interfaz básica para interactuar con la API de GitHub Classroom, permitiendo listar asignaciones aceptadas y clonar repositorios de estudiantes.