from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from pdf2image import convert_from_path
import os
import cv2
import gpt
from PIL import Image
from util import crop_image

if __name__ == "__main__":
    # Authenticate and initialize PyDrive
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()  # Creates local webserver and auto handles authentication
    drive = GoogleDrive(gauth)

    # List all files in a specified directory (folder)
    folder_id = '1UCMqoqjN_ZlqVDRHJkzkb8hzi8m-ehJm'  # Student Work folder in engg130aimarking@gmail.com
    query = f"'{folder_id}' in parents and trashed=false"

    # Fetch the list of all files in the folder
    file_list = drive.ListFile({'q': query}).GetList()

    # Download and read each image
    for file in file_list:
        if file['mimeType'].startswith('application/pdf'):  # Check if the file is an pdf
            file_name = file['title']
            print(f'Downloading {file_name}...')
            file.GetContentFile(file_name)  # Download the file

            # Convert PDF to images
            images = convert_from_path(file_name)

            # Save each page as an image
            image_list = []
            for i, image in enumerate(images):
                image_path = f'{"./temp/"+file_name.strip(".pdf")}_{i + 1}.png'
                image.save(image_path, 'PNG')
                print(f'Saved {image_path}')
                image_list.append(image_path)
                break

            # Remove the pdf after processing
            os.remove(file_name)

            # Read every page in pdf
            for image_path in image_list:
                # response = gpt.process(image_path)
                # print(response)
                image = crop_image(image_path)
                image.save(f".{image_path.strip('.png')}_cropped.png")
                # image.show()
                # image = cv2.imread(image_path)
                # cv2.imshow('Image', image)
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()
                # os.remove(image_path)



