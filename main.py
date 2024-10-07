import os
import pandas as pd
from PIL import Image
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from pdf2image import convert_from_path
import gpt
from util import crop_lab, extract_name, save_to_excel

def authenticate():
    # Authenticate and initialize PyDrive
    gauth = GoogleAuth()
    gauth.LoadClientConfigFile('secrets/client_secrets.json')
    gauth.LocalWebserverAuth()  # Creates local webserver and auto handles authentication
    drive = GoogleDrive(gauth)
    return drive

def list_files(drive, folder_id):
    # List all files in a specified directory (folder)
    query = f"'{folder_id}' in parents and trashed=false"
    # Fetch the list of all files in the folder
    file_list = drive.ListFile({'q': query}).GetList()
    return file_list

def download_pdf(file, download_dir):
    pdf = file['title']
    print(f'Downloading {pdf}...')
    file.GetContentFile(os.path.join(download_dir, pdf))  # Download the file to the specified directory

def convert_pdf_to_images(download_dir, pdf):
    # Convert PDF to images
    images = convert_from_path(f"{download_dir+pdf}")
    # Save each page as an image
    image_list = []
    for i, image in enumerate(images):
        image_path = f'{download_dir+pdf.strip(".pdf")}_{i + 1}.png'
        image.save(image_path, 'PNG')
        print(f'Saved {image_path}')
        image_list.append(image_path)
    return image_list

def process_images(image_list, df, random_id):
    for page, image_path in enumerate(image_list):
        image = crop_lab(image_path)
        cropped_img_path = f"./temp/{random_id}_{page+1}.png"
        os.remove(image_path)
        image.save(cropped_img_path)
        response = gpt.digitize(cropped_img_path)
        # Write response to a text file
        with open(f"./digitized/{random_id}_{page}.txt", "w") as text_file:
            text_file.write(str(response['choices'][0]['message']['content']))
        page += 1

def main():
    # Authenticate and initialize PyDrive
    drive = authenticate()

    # List all files in a specified directory (folder)
    folder_id = '1UCMqoqjN_ZlqVDRHJkzkb8hzi8m-ehJm'  # Student Work folder in engg130aimarking@gmail.com
    file_list = list_files(drive, folder_id)

    # Create a DataFrame to store the extracted student ID and names
    df = pd.DataFrame(columns=['Name', 'ID', 'random_ID', 'Grade'])

    # Download and process each PDF
    for file in file_list:
        if file['mimeType'].startswith('application/pdf'):  # Check if the file is a PDF
            download_dir = "./pdfs/"  # Specify the directory to download the file
            download_pdf(file, download_dir)
            image_list = convert_pdf_to_images(download_dir, file['title'])
            df, random_id = extract_name(image_list[0], df)
            os.rename(f"{download_dir+file['title']}", f"{download_dir+str(random_id)}.pdf")
            process_images(image_list, df, random_id)
            save_to_excel(df)

if __name__ == "__main__":
    main()
