import ocr_utils
import process
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

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

if __name__ == "__main__":
    # Prompt the user to select the option
    print("Select an option:")
    print("1 - Crop Labs and Extract Names (Google Drive)")
    print("2 - Crop Labs and Extract Names (Shared Network)")
    print("q - Quit")
    print("")
    option = input()
    while True:
        if option == '1':
            option2_gdrive()
            break
        elif option == '2':
            option2_smb()
            break
        elif option == 'q':
            break
        else:
            option = input("Invalid option")
            continue

