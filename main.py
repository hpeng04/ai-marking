import os
import pandas as pd
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import gpt
import gemini # TBD
import process
import io_utils

def authenticate():
    # Authenticate and initialize PyDrive
    gauth = GoogleAuth()
    gauth.LoadClientConfigFile('secrets/client_secrets.json')
    gauth.LocalWebserverAuth()  # Creates local webserver and auto handles authentication
    drive = GoogleDrive(gauth)
    return drive

def option1():
    # Authenticate and initialize PyDrive
    drive = authenticate()

    solutions_folder_id = r'1h5pJGGLeARTLeRaMMslnDll8pwF16XR8'
    students_work_folder_id = r'1UCMqoqjN_ZlqVDRHJkzkb8hzi8m-ehJm'

    # List all files in the Google Drive folder
    student_file_list = process.list_files_gdrive(drive, students_work_folder_id)
    solution_file_list = process.list_files_gdrive(drive, solutions_folder_id)

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

def option2():

    solutions_folder_path = r'/Volumes/engg-130research/Solutions'
    students_work_folder_path = r'/Volumes/engg-130research/Student Work'

    # Get file list from the shared network folder
    solutions_file_list= process.list_files_smb(solutions_folder_path)
    students_file_list = process.list_files_smb(students_work_folder_path)

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


def option3():
    # For every student work in digitized/ folder, mark the lab

    # Path to solution file
    solution_path = r'solutions/Lab 1 Solutions A.pdf.txt' # To be changed to dynamic path

    df = io_utils.read_excel_to_dataframe('data/student_data.xlsx')
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

def main():
    
    while True:
        # Prompt the user to choose the option for running the program
        # 1 - Process Google Drive PDFs
        # 2 - Process Shared Network PDFs
        # 3 - Process Digitized Texts Only
        option = input("Select an option:\n1 - Process Google Drive PDFs\n2 - Process Shared Network PDFs\n3 - Process Digitized Texts Only\n")
        if option == '1': # Process PDFs and digitized texts
            option1()
            break
        
        if option == '2':
            option2()
            break

        elif option == '3': # Process digitized texts only
            option3()
            break
        else:
            print("Invalid option")

if __name__ == "__main__":
    main()


# To do:
# Finalize LLM and VLM models
# Reconfigure the framework the fit the LLM and VLM models
# Refine Prompts
# Test the system