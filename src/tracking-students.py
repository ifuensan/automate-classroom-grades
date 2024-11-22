import requests
from github import Github

# Función para obtener el número de issues abiertas por un usuario en un repositorio
def get_open_issues(repo, username):
    issues = repo.get_issues(state='open', creator=username)
    return issues.totalCount

# Función para obtener el número de PRs abiertas por un usuario en un repositorio
def get_open_prs(repo, username):
    prs = repo.get_pulls(state='open')
    # Si necesitas filtrar por creador después de obtener todos los PRs:
    # user_prs = [pr for pr in prs if pr.user.login == username]    
    return prs.totalCount

def get_commits(repo, username):
    commits = repo.get_commits()  # Obtener todos los commits del repositorio
    # Si deseas filtrar por autor, puedes utilizar:
    user_commits = [commit for commit in commits if commit.author.login == username]
    return user_commits

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
    
    commits_count = get_commits(repo, username)
    
    return {
        'username': username,
        'repo': repo_name,
        'open_issues': issues_count,
        'open_prs': prs_count,
        'comments': comments_count,
        'commits': len(commits_count)
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
        print(f"Commits: {activity['commits']}")
        print(f"Comentarios: {activity['comments']}")
        print("")

if __name__ == "__main__":
    main()