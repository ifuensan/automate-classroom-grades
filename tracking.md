### Plan

https://github.com/PyGithub/PyGithub

1. **Recibir URLs de los proyectos y nombres de usuario de GitHub**:
    - Crear una función para recibir las URLs de los proyectos y los nombres de usuario de GitHub.

2. **Obtener datos de actividad de los usuarios**:
    - Crear funciones para obtener el número de issues abiertas, PRs abiertas, y comentarios de cada usuario en los proyectos especificados.

3. **Mostrar los resultados**:
    - Crear una función para mostrar los resultados de la actividad de cada usuario.

### Código

Aquí tienes un script en Python que realiza el seguimiento de la actividad de los alumnos en los proyectos de GitHub especificados:

```python
import requests
from github import Github

# Función para obtener el número de issues abiertas por un usuario en un repositorio
def get_open_issues(repo, username):
    issues = repo.get_issues(state='open', creator=username)
    return issues.totalCount

# Función para obtener el número de PRs abiertas por un usuario en un repositorio
def get_open_prs(repo, username):
    prs = repo.get_pulls(state='open', creator=username)
    return prs.totalCount

# Función para obtener el número de comentarios de un usuario en un repositorio
def get_comments(repo, username):
    comments = repo.get_issues_comments()
    user_comments = [comment for comment in comments if comment.user.login == username]
    return len(user_comments)

# Función para obtener la actividad de un usuario en un repositorio
def get_user_activity(repo_url, username, token):
    g = Github(token)
    repo_name = repo_url.split('github.com/')[-1].replace('.git', '')
    repo = g.get_repo(repo_name)
    
    issues_count = get_open_issues(repo, username)
    prs_count = get_open_prs(repo, username)
    comments_count = get_comments(repo, username)
    
    return {
        'username': username,
        'repo': repo_name,
        'open_issues': issues_count,
        'open_prs': prs_count,
        'comments': comments_count
    }

# Función principal para recibir las URLs de los proyectos y los nombres de usuario de GitHub
def main():
    token = input("Introduce tu token de GitHub: ")
    num_students = int(input("Introduce el número de estudiantes: "))
    
    students_data = []
    for _ in range(num_students):
        username = input("Introduce el nombre de usuario de GitHub del estudiante: ")
        repo_url = input("Introduce la URL del repositorio del proyecto: ")
        students_data.append((repo_url, username))
    
    for repo_url, username in students_data:
        activity = get_user_activity(repo_url, username, token)
        print(f"Actividad de {username} en {activity['repo']}:")
        print(f"Issues abiertas: {activity['open_issues']}")
        print(f"PRs abiertas: {activity['open_prs']}")
        print(f"Comentarios: {activity['comments']}")
        print("")

if __name__ == "__main__":
    main()
```

### Explicación

1. **Importación de Módulos**:
    - `requests`: Para realizar solicitudes HTTP.
    - `github`: Para interactuar con la API de GitHub.

2. **Funciones para Obtener Datos de Actividad**:
    - `get_open_issues`: Obtiene el número de issues abiertas por un usuario en un repositorio.
    - `get_open_prs`: Obtiene el número de PRs abiertas por un usuario en un repositorio.
    - `get_comments`: Obtiene el número de comentarios de un usuario en un repositorio.

3. **Función `get_user_activity`**:
    - Recibe la URL del repositorio, el nombre de usuario y el token de GitHub.
    - Utiliza la API de GitHub para obtener el repositorio y los datos de actividad del usuario.

4. **Función Principal `main`**:
    - Solicita al usuario que introduzca su token de GitHub y el número de estudiantes.
    - Recibe las URLs de los proyectos y los nombres de usuario de GitHub de los estudiantes.
    - Llama a `get_user_activity` para cada estudiante y muestra los resultados.

### Ejecución del Script

Para ejecutar el script, asegúrate de tener instalado el módulo `PyGithub`:

```bash
pip install PyGithub
```

Luego, ejecuta el script:

```bash
python seguimiento_alumnos.py
```

Introduce tu token de GitHub, el número de estudiantes, y las URLs de los proyectos y los nombres de usuario de GitHub cuando se te solicite. El script mostrará la actividad de cada estudiante en los proyectos especificados.