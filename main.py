from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from pdf2image import convert_from_path
import os
import cv2
import gpt
from PIL import Image
from util import crop_lab, extract_name, save_to_excel
import pandas as pd

def main():
    # Authenticate and initialize PyDrive
    gauth = GoogleAuth()
    gauth.LoadClientConfigFile('secrets/client_secrets.json')
    gauth.LocalWebserverAuth()  # Creates local webserver and auto handles authentication
    drive = GoogleDrive(gauth)

    # List all files in a specified directory (folder)
    folder_id = '1UCMqoqjN_ZlqVDRHJkzkb8hzi8m-ehJm'  # Student Work folder in engg130aimarking@gmail.com
    query = f"'{folder_id}' in parents and trashed=false"

    # Fetch the list of all files in the folder
    file_list = drive.ListFile({'q': query}).GetList()

    # Create a DataFrame to store the extracted student ID and names
    df = pd.DataFrame(columns=['Name', 'ID', 'random_ID'])

    # Download and read each image
    for file in file_list:
        if file['mimeType'].startswith('application/pdf'):  # Check if the file is an pdf
            pdf = file['title']
            print(f'Downloading {pdf}...')
            download_dir = "./temp/"  # Specify the directory to download the file
            file.GetContentFile(os.path.join(download_dir, pdf))  # Download the file to the specified directory

            # Convert PDF to images
            images = convert_from_path(f"./temp/{pdf}")

            # Save each page as an image
            image_list = []
            for i, image in enumerate(images):
                image_path = f'{"./temp/"+pdf.strip(".pdf")}_{i + 1}.png'
                image.save(image_path, 'PNG')
                print(f'Saved {image_path}')
                image_list.append(image_path)
                break

            # Remove the pdf after processing
            os.remove(f"./temp/{pdf}")

            df, random_id = extract_name(image_list[0], df)
            save_to_excel(df)

            # Read every page in pdf
            page = 1
            for image_path in image_list:
                # response = gpt.process(image_path)
                # print(response)
                image = crop_lab(image_path)
                image.save(f"./temp/{random_id}_{page}.png")
                page += 1
                # image.show()
                # image = cv2.imread(image_path)
                # cv2.imshow('Image', image)
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()
                # os.remove(image_path)

if __name__ == "__main__":
    main()