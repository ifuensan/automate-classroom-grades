import os
from time import sleep
import pandas as pd

def get_classroom_id(classroom_name):
    # Get the list of repositories using the GitHub CLI
    classrooms = os.popen('gh classroom list').read()
    # Split the classrooms by newline character
    classrooms = classrooms.split('\n')
    # Remove the first two lines (header and separator)
    classrooms = classrooms[3:]
    # Loop through each repository
    #print(classrooms)
    for classroom in classrooms:
        # Split the classroom details by whitespace
        classroom_details = classroom.split()
        #print(classroom_details)
        # Get the classroom ID and name
        classroom_id = classroom_details[0]
        classroom_name = classroom_details[1]
        # Check if the classroom name matches the one you send
        if classroom_name == classroom_name:
            return classroom_id
    # Return None if the classroom is not found
    return None

def get_assignments(classroom_id):
    # Run the command to get assignments for the given classroom ID using the GitHub CLI
    assignments = os.popen(f'gh classroom assignments -c {classroom_id}').read()
    # Process the output and extract the assignment details
    # Split the assignments by newline character
    assignments = assignments.split('\n')
    # Remove the first two lines (header and separator)
    assignments = assignments[3:-1]
    # Loop through each assignment
    assignment_data = []
    for assignment in assignments:
        # Split the assignment details by tab character
        assignment_details = assignment.split('\t')
        # Get the assignment ID, name, and repository
        assignment_id = assignment_details[0]
        assignment_name = assignment_details[1]
        assignment_repo = assignment_details[6]
        assignment_data.append((assignment_id, assignment_name, assignment_repo))
    return assignment_data

def download_grades(assignment_id):
    # Get the file of one assignment id using the GitHub CLI
    directory = "csvs"
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_grades = f"{directory}/{assignment_id}.csv"
    
    try:
        file_grades = os.popen(f'gh classroom assignment-grades -a {assignment_id} -f {file_grades}').read()
        sleep(5)
        return file_grades
    except Exception as e:
        print(f"Error occurred while downloading grades: {str(e)}")

def parse_csv(file_path):
    try:
        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(file_path) 
        # Process the DataFrame as needed
        github_username = df['github_username']
        points_awarded = df['points_awarded']
        points_available = df['points_available']
        # Or iterate over the rows like this:
        for index, row in df.iterrows():
            github_username = row['github_username']
            points_awarded = row['points_awarded']
            points_available = row['points_available']
            # Process the assignment data
            print(f"User Name: {github_username}")
            print(f"Points Awarded: {points_awarded}")
            print(f"Points Available: {points_available}")
    except FileNotFoundError as e:
        print(f"Error occurred while parsing CSV: {str(e)}")
    
if __name__ == "__main__":
    # Call the function to get the classroom ID
    classroom_id = get_classroom_id("B4OS-Dev-classroom")
    print(f"Classroom ID: {classroom_id}")
    assignment_data = get_assignments(classroom_id)
    print(f"Assignment Data: {assignment_data[0][0]}")
    file_grades = download_grades(assignment_data[0][0])
    parse_csv(file_grades)
    
