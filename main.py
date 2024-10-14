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

def main():
    # Authenticate and initialize PyDrive
    while True:
        # Prompt the user to choose the option for running the program
        # 1 - Process PDFs
        # 2 - Process Digitized Texts Only
        option = input("Select an option:\n1 - Process PDFs\n2 - Process Digitized Texts Only\n")
        if option == '1': # Process PDFs and digitized texts

            drive = authenticate()

            solutions_folder_id = r'1h5pJGGLeARTLeRaMMslnDll8pwF16XR8'
            students_work_folder_id = r'1UCMqoqjN_ZlqVDRHJkzkb8hzi8m-ehJm'

            # Processes the solutions by digitizing the solution PDF using LLMs
            # and saving it to a text file with the path solution_path
            solution_path = process.process_solutions(drive, solutions_folder_id)

            # Processes all student labs by digitizing the student work PDFs using LLMs
            # and stores the student information along with their random id in a dataframe
            # and excel file in data/student_data.xlsx
            df = process.process_student_work(drive, students_work_folder_id)
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
            break

        elif option == '2': # Only process the digitized texts
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