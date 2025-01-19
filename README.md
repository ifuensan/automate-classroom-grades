# Automate Github Classroom Grades Reports

## GitHub Classroom CLI

The `gh-classroom` plugin is an extension for the GitHub command-line tool (`gh`) that makes it easy to manage assignments and student repositories in GitHub Classroom. With this plugin, you can list assignments, clone student repositories, and obtain grades easily and efficiently.

### Install

To install the `gh-classroom` plugin, run the following command:

```bash
gh extension install github/gh-classroom
```

This command will download and install the `gh-classroom` extension around `gh`, allowing you to use the additional commands provided by the plugin.

In this repository I intend to make a summary of the main commands that I will later use for the program, but [here](https://github.com/github/gh-classroom) you can find a much more complete explanation of the plugin.

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

The `gh classroom accepted-assignments` command is used to list accepted assignments in GitHub Classroom. Below is a detailed explanation of how to use this command:

```bash
gh classroom accepted-assignments
```
Without additional arguments, this command displays a list of all accepted assignments in your GitHub Classroom.

#### Usage Examples

If you want to skip the selection step and directly specify the assignment ID, you can use the `-a` option followed by the assignment ID. Here are two examples:

```bash
gh classroom accepted-assignments -a 605580 # accepted assignment id
gh classroom clone student-repos -a 612817 # student repo id
```

- **`gh classroom accepted-assignments -a 605580`**: Lists the accepted assignments for the assignment with ID `605580`.  
- **`gh classroom clone student-repos -a 612817`**: Clones the student repositories for the assignment with ID `612817`.

### Python Program Explanation

Below is an explanation of the Python code for this project. The main file is `download-grades.py`, which contains the following functions:

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

#### Code Explanation

1. **Module Import**:  
    - `import requests`: Imports the `requests` module to make HTTP requests.

2. **Function `get_accepted_assignments`**:  
    - **Parameters**:  
        - `api_url`: The base URL of the GitHub Classroom API.  
        - `assignment_id`: (Optional) The ID of the assignment.  
    - **Description**:  
        - Constructs the URL to fetch accepted assignments.  
        - Sends a GET request to the API.  
        - If the response is successful (status code 200), it returns the data in JSON format.  
        - If an error occurs, it raises an exception with the response's status code.  

3. **Function `clone_student_repos`**:  
    - **Parameters**:  
        - `api_url`: The base URL of the GitHub Classroom API.  
        - `assignment_id`: The ID of the assignment.  
    - **Description**:  
        - Constructs the URL to clone student repositories.  
        - Sends a POST request to the API.  
        - If the response is successful (status code 200), it returns the data in JSON format.  
        - If an error occurs, it raises an exception with the response's status code.  

4. **Main Block**:  
    - Defines the API's base URL and the assignment ID.
    - Attempts to fetch accepted assignments and clone student repositories.
    - Prints the results or the error if an exception occurs.  

This code provides a basic interface to interact with the GitHub Classroom API, allowing you to list accepted assignments and clone student repositories.

Under development the [Tracking[() section.
