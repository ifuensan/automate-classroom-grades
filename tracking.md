### Plan

https://github.com/PyGithub/PyGithub

1. **Receive URLs of projects and GitHub usernames:**
    - Create a function to receive the URLs of the projects and the GitHub usernames.

2. **Get user activity data:**
    - Create functions to get the number of open issues, open PRs, and comments from each user in the specified projects.
3. **Display the results:**
    - Create a function to display the activity results of each user.

### Code

Here is a Python script that tracks the activity of students in the specified GitHub projects:

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

### Reason

1. **Module Import:**
- `requests`: To make HTTP requests.
- `github`: To interact with the GitHub API.


2. **Functions to Get Activity Data**:
    - `get_open_issues`: Gets the number of open issues by a user in a repository.
    - `get_open_prs`: Gets the number of open PRs by a user in a repository.
    - `get_comments`: Gets the number of comments by a user in a repository.

3. **Function `get_user_activity`**:
    - Receives the repository URL, the username, and the GitHub token.
    - Uses the GitHub API to get the repository and the activity data of the user.

4. **Principal Function `main`**:
    - Asks the user to enter their GitHub token and the number of students.
    - Receives the URLs of the projects and the GitHub usernames of the students.
    - Calls `get_user_activity` for each student and displays the results.

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
