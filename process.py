from ocr_utils import crop_lab, extract_name
import gpt
import os
import pandas as pd
import io_utils
import re
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import shutil

# List the files contained the Google Drive folder
def list_files_gdrive(drive, folder_id):
    # List all files in a specified directory (folder)
    query = f"'{folder_id}' in parents and trashed=false"
    # Fetch the list of all files in the folder
    file_list = drive.ListFile({'q': query}).GetList()
    return file_list

def list_files_smb(folder_path):
  # List all files and directories in the specified directory
    all_entries = os.listdir(folder_path)
    
    # Create full path for each file and filter out only the files
    full_paths = [os.path.join(folder_path, entry) for entry in all_entries if os.path.isfile(os.path.join(folder_path, entry))]
    # print(full_paths)
    return full_paths

# Download the PDF from the Google Drive to a specified directory download_dir
def download_pdf(file, download_dir):
    pdf = file['title']
    print(f'Downloading {pdf}...')
    file.GetContentFile(os.path.join(download_dir, pdf))  # Download the file to the specified directory

# Process the images with the LLM and save the digitized text to a text file
# in the directory digitized/
def process_images(image_list, random_id):
    for page, image_path in enumerate(image_list):
        image = crop_lab(image_path)
        cropped_img_path = f"temp/{random_id}_{page+1}.png"
        os.remove(image_path)
        image.save(cropped_img_path)
        response = gpt.digitize_student_work(cropped_img_path)
        # Write response to a text file
        with open(f"digitized/{random_id}.txt", "a") as text_file:
            text_file.write(str(response))
        page += 1

# Process the solution PDF images with the LLM and save the digitized text to a text file
# This is different from process_images as it requires a different prompt
def process_images_solution(image_list, solution_dir):
    for page, image_path in enumerate(image_list):
        response = gpt.digitize_solution(image_path)

        # Write response to a text file
        with open(solution_dir, "a") as text_file:
            text_file.write(str(response))
            text_file.write("\n")

        page += 1

# Process each PDF in the solutions folder
# Multiple solution PDFs DOES NOT work at the moment
# Multiple solution PDFs function to be implemented
def process_solutions_gdrive(file_list):
    for file in file_list:
        if file['mimeType'].startswith('application/pdf'):  # Check if the file is a PDF

            # Get file name
            file_name = file['title']

            solution_path = f"solutions/{file_name}.txt"
            
            download_dir = "solutions/"  # Specify the directory to download the file
            download_pdf(file, download_dir)
            image_list = io_utils.pdf2imagelist(download_dir, file['title'])
            process_images_solution(image_list, solution_path)

    return solution_path

def process_solutions_smb(file_list):
    for file in file_list:
        if file.endswith('.pdf'):  # Check if the file is a PDF

            # Get file name
            file_name = os.path.basename(file).split('.')[0]

            solution_path = f"solutions/{file_name}.txt"
            download_dir = "solutions/"  # Specify the directory to download the file
            
            shutil.copy(file, download_dir)
            print(f"Saved {file_name}.pdf")

            image_list = io_utils.pdf2imagelist(download_dir, file_name+'.pdf')
            

            process_images_solution(image_list, solution_path)

    return solution_path

# Processes all student lab PDFs downloaded in the dir pdfs/
def process_student_work_gdrive(file_list):
    # Create a DataFrame to store the extracted student ID and names
    df = pd.DataFrame(columns=['Name', 'ID', 'random_ID', 'Grade'])

    # Download and process each student's work PDF
    for file in file_list:
        if file['mimeType'].startswith('application/pdf'):  # Check if the file is a PDF
            download_dir = "pdfs/"  # Specify the directory to download the file
            download_pdf(file, download_dir)
            image_list = io_utils.pdf2imagelist(download_dir, file['title'])

            # Extract the student name and ID from the first page with OCR
            # To be replaced by file naming.
            df, random_id = extract_name(image_list[0], df)
            os.rename(f"{download_dir+file['title']}", f"{download_dir+str(random_id)}.pdf")

            process_images(image_list, random_id)

            io_utils.save_to_excel(df)
    return df

def process_student_work_smb(file_list):
    # Create a DataFrame to store the extracted student ID and names
    df = pd.DataFrame(columns=['Name', 'ID', 'random_ID', 'Grade'])

    # Download and process each student's work PDF
    for file in file_list:
        if file.endswith('.pdf'):  # Check if the file is a PDF
            download_dir = "pdfs/"  # Specify the directory to download the file
            shutil.copy(file, download_dir)
            
            print(f"Saved {os.path.basename(file)}")

            image_list = io_utils.pdf2imagelist(download_dir, os.path.basename(file))

            # Extract the student name and ID from the first page with OCR
            # To be replaced by file naming.
            df, random_id = extract_name(image_list[0], df)
            os.rename(f"{download_dir+os.path.basename(file)}", f"{download_dir+str(random_id)}.pdf")

            process_images(image_list, random_id)

            io_utils.save_to_excel(df)
    return df

def retrieve_mark(feedback):
    mark = feedback.splitlines()[-1]
    mark = re.findall(r'\d+', mark)
    mark = ''.join(mark)
    mark = int(mark)
    return mark