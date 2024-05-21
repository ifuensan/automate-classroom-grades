import os
from time import sleep
import pandas as pd
import datetime
import glob

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

def download_grades(assignment_id, path):
    # Get the file of one assignment id using the GitHub CLI
    directory = path
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_grades_dir = f"{directory}/{assignment_id}.csv"
    
    try:
        file_grades = os.popen(f'gh classroom assignment-grades -a {assignment_id} -f {file_grades_dir}').read()
        # Check if the file exists
        if os.path.isfile(file_grades_dir):
            return file_grades_dir, True
        else:
            return file_grades_dir, False
    except Exception as e:
        print(f"Error occurred while downloading grades: {str(e)}")
        #return file_grades_dir, False

def parse_csv(file_path):
    try:
        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(file_path) 
        # Process the DataFrame as needed
        github_username = df['github_username']
        points_awarded = df['points_awarded']
        points_available = df['points_available']
        # Or iterate over the rows like this:
        df_sorted = df.sort_values(by='points_awarded', ascending=False)
        print(f"{'github_username':<20} {'points_awarded':>2}/{'points_available'}") 
        for index, row in df_sorted.iterrows():
            github_username = row['github_username']
            points_awarded = row['points_awarded']
            points_available = row['points_available']
            # Process the assignment data
            print(f"{github_username:<20} {points_awarded:>2}/{points_available}")
        return df_sorted
    except FileNotFoundError as e:
        print(f"Error occurred while parsing CSV: {str(e)}")

# Function to delete old CSV files
def delete_old_csv_files(path):
    old_files = glob.glob(path + "*.csv")
    for file in old_files:
        os.remove(file)

def format_assignment_name(name):
    # Eliminar espacios y unir palabras con guiones
    name = name.replace(' ', '-')
    
    # Limitar la longitud a 30 caracteres
    return name[:30]

def download_grades_for_assignments(assignment_data, path):
    print("Downloading grades...")
    for assignment in assignment_data:
        assignment_id = assignment[0]
        file_grades_dir, f_exists = download_grades(assignment_id, path)
        if f_exists:
            print(f"Assignment {assignment_id}.")

def consolidate_grades(path):
    # Get the list of new CSV files
    all_files = sorted(glob.glob(path + "*.csv"), key=lambda x: x.split('/')[-1])

    print("Consolidating grades...")
    consolidated_df = pd.DataFrame()
    for filename in all_files:
        df = pd.read_csv(filename)
        assignment_id = filename.split('/')[-1].split('.')[0]
        assignment_name = format_assignment_name(df['assignment_name'].iloc[0]) 
        print(f"Assignment {assignment_id} - {assignment_name}")
        df = df[['github_username', 'points_awarded', 'points_available']]
        df = df.rename(columns={'points_awarded': f'paw_{assignment_name}',
                                'points_available': f'pav_{assignment_name}'})
        if consolidated_df.empty:
            consolidated_df = df
        else:
            consolidated_df = pd.merge(consolidated_df, df, on='github_username', how='outer')

    # Save the consolidated DataFrame to an Excel file
    date_string = datetime.datetime.now().strftime("%Y%m%d")
    file_name = f'consolidated_assignments_{date_string}.xlsx'
    consolidated_df.to_excel(file_name, index=False)

if __name__ == "__main__":
    # Path to the CSVs
    path = 'csvs/'

    # Delete old CSV files
    delete_old_csv_files(path)

    # Call the function to get the classroom ID
    classroom_id = get_classroom_id("B4OS-Dev-classroom")
    print(f"Classroom ID: {classroom_id}")
    assignment_data = get_assignments(classroom_id)

    # Download grades for each assignment
    download_grades_for_assignments(assignment_data, path)

    # Consolidate grades
    consolidate_grades(path)
