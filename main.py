import os
import pandas as pd
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import gpt
import gemini # TBD
import process
import io_utils

CLEAR = r'clear' if os.name == 'posix' else 'cls'

STUDENT_FOLDER_ID_GDRIVE = r'1UCMqoqjN_ZlqVDRHJkzkb8hzi8m-ehJm'
SOLUTION_FOLDER_ID_GDRIVE = r'1h5pJGGLeARTLeRaMMslnDll8pwF16XR8'
SOLUTION_FOLDER_PATH_SMB = r'/Volumes/engg-130research/Solutions'
STUDENT_FOLDER_PATH_SMB = r'/Volumes/engg-130research/Student Work'
SOLUTION_PATH = r'solution/Lab 1 Solutions A.txt'

def authenticate():
    # Authenticate and initialize PyDrive
    gauth = GoogleAuth()
    gauth.LoadClientConfigFile('secrets/client_secrets.json')
    gauth.LocalWebserverAuth()  # Creates local webserver and auto handles authentication
    drive = GoogleDrive(gauth)
    return drive

# Processes the Google Drive PDFs
def option1_gdrive():
    # Authenticate and initialize PyDrive
    drive = authenticate()

    # List all files in the Google Drive folder
    student_file_list = process.list_files_gdrive(drive, STUDENT_FOLDER_ID_GDRIVE)
    solution_file_list = process.list_files_gdrive(drive, SOLUTION_FOLDER_ID_GDRIVE)

    # Processes the solutions by digitizing the solution PDF using LLMs
    # and saving it to a text file with the path solution_path
    solution_path = process.process_solutions_gdrive(solution_file_list)

    # Processes all student labs by digitizing the student work PDFs using LLMs
    # and stores the student information along with their random id in a dataframe
    # and excel file in data/student_data.xlsx
    df = process.process_student_work_gdrive(student_file_list)
    for file in os.listdir("digitized/"):
        if file.endswith('.txt'):

            # Call LLM for marking and providing feedback
            feedback = gpt.mark_lab(solution_path, f'digitized/{file}')

            # Create feedback file for random id associated to student
            with open(f"feedback/{file}", "w") as text_file:
                text_file.write(str(feedback))

            # Retrieve the mark from the feedback and save to dataframe and excel
            mark = process.retrieve_mark(feedback)
            io_utils.save_mark(mark, df, file.strip('.txt'))
    return

# Processes the shared network PDFs
def option1_smb():

    # Get file list from the shared network folder
    solutions_file_list= process.list_files_smb(SOLUTION_FOLDER_PATH_SMB)
    students_file_list = process.list_files_smb(STUDENT_FOLDER_PATH_SMB)

    # Processes the solutions by digitizing the solution PDF using LLMs
    # and saving it to a text file with the path solution_path
    solution_path = process.process_solutions_smb(solutions_file_list)

    # Processes all student labs by digitizing the student work PDFs using LLMs
    # and stores the student information along with their random id in a dataframe
    # and excel file in data/student_data.xlsx
    df = process.process_student_work_smb(students_file_list)
    for file in os.listdir("digitized/"):
        if file.endswith('.txt'):

            # Call LLM for marking and providing feedback
            feedback = gpt.mark_lab(solution_path, f'digitized/{file}')

            # Create feedback file for random id associated to student
            with open(f"feedback/{file}", "w") as text_file:
                text_file.write(str(feedback))

            # Retrieve the mark from the feedback and save to dataframe and excel
            mark = process.retrieve_mark(feedback)
            io_utils.save_mark(mark, df, file.strip('.txt'))
    return

# Crop labs and extract names Google Drive
def option2_gdrive():
    drive = authenticate()

    # List all files in the Google Drive folder
    student_file_list = process.list_files_gdrive(drive, STUDENT_FOLDER_ID_GDRIVE)

    process.process_student_work_gdrive(student_file_list)

    return
    

# Crop labs and extract names Shared Network
def option2_smb():
    # Get file list from the shared network folder
    students_file_list = process.list_files_smb(STUDENT_FOLDER_PATH_SMB)

    process.process_student_work_smb(students_file_list)

    return

# Processes the digitized texts only
def option3():
    # For every student work in digitized/ folder, mark the lab and provide feedback
    df = io_utils.read_excel_to_dataframe('data/student_data.xlsx')
    for file in os.listdir("digitized/"):
        if file.endswith('.txt'):

            # Call LLM for marking and providing feedback
            feedback = gpt.mark_lab(SOLUTION_PATH, f'digitized/{file}')

            # Create feedback file for random id associated to student
            with open(f"feedback/{file}", "w") as text_file:
                text_file.write(str(feedback))

            # Retrieve the mark from the feedback and save to dataframe and excel
            mark = process.retrieve_mark(feedback)
            io_utils.save_mark(mark, df, file.strip('.txt'))
    return

def main():
    
    while True:
        # Prompt the user to choose the option for running the program
        # 1 - Process Google Drive PDFs
        # 2 - Process Shared Network PDFs
        # 3 - Process Digitized Texts Only
        os.system(CLEAR)
        option = input("Select an option:\n1 - Process PDFs\n2 - Crop Labs and Extract Names\n3 - Process Digitized Texts Only (Local)\nq - Quit\n")
        if option == '1': # Process PDFs and digitized texts
            while True:
                os.system(CLEAR)
                file_loc = input("Select the location of the PDFs:\n1 - Google Drive\n2 - Shared Network\nb - Back\nq - Quit\n")
                if file_loc == '1': # Google Drive
                    option1_gdrive()
                    exit()
                elif file_loc == '2': # Shared Network
                    option1_smb()
                    exit()
                elif file_loc == 'b': # Back to the main menu
                    option = ''
                    break
                elif file_loc == 'q': # Quit the program
                    os.system(CLEAR)
                    exit()
                else:
                    print("Invalid option")
        
        if option == '2': # Crop labs and extract names
            while True:
                os.system(CLEAR)
                file_loc = input("Select the location of the PDFs:\n1 - Google Drive\n2 - Shared Network\nb - Back\nq - Quit\n")
                if file_loc == '1': # Google Drive
                    option2_gdrive()
                    exit()
                elif file_loc == '2': # Shared Network
                    option2_smb()
                    exit()
                elif file_loc == 'b': # Back to the main menu
                    option = ''
                    break
                elif file_loc == 'q': # Quit the program
                    os.system(CLEAR)
                    exit()
                else:
                    print("Invalid option")
        elif option == '3':  # Process digitized texts only
            option3()
            break
        elif option == 'q': # Quit the program
            os.system(CLEAR)
            exit()
        elif option == '':
            continue
        else:
            print("Invalid option")

if __name__ == "__main__":
    main()


# To do:
# Finalize LLM and VLM models
# Reconfigure the framework the fit the LLM and VLM models
# Refine Prompts
# Test the system