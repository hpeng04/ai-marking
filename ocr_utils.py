from PIL import Image, ImageFilter, ImageOps
import pytesseract
import cv2
import numpy as np
import re
import pandas as pd
import os
import io_utils

def crop_name(img_path, random_id):
    with Image.open(img_path) as img:
        width, height = img.size
        name_crop = img.crop((3/5*width, 0, width*0.93, height*0.1))
        name_crop.save(f"./temp/{random_id}_name.png")
    return name_crop

# Preprocess the image by straightening, sharpening, denoising, and binarization
def preprocess_image(img):
    # Convert to grayscale
    gray = ImageOps.grayscale(img)
    
    # Convert to numpy array for OpenCV processing
    img_array = np.array(gray)
    
    # Apply thresholding
    _, thresh = cv2.threshold(img_array, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    
    # Remove noise
    kernel = np.ones((1, 1), np.uint8)
    processed_img = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    
    # Convert back to PIL Image
    processed_img = Image.fromarray(processed_img)
    
    # Sharpen the image
    sharpened_img = processed_img.filter(ImageFilter.SHARPEN)
    
    # Denoise the image
    denoised_img = cv2.fastNlMeansDenoising(np.array(sharpened_img), None, 10, 7, 21)
    
    # Binarize the image
    _, binarized_img = cv2.threshold(denoised_img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    
    # Convert back to PIL Image
    preprocessed_img = Image.fromarray(binarized_img)
    
    return preprocessed_img

### PLACEHOLDER ###
### To be replaced by other vision models ###
def perform_ocr(img): 
    # Preprocess the image
    processed_img = preprocess_image(img)
    
    # Perform OCR on the image
    extracted_text = pytesseract.image_to_string(processed_img, config="--psm 7", lang='eng')
    
    # Print the extracted text
    # processed_img.show()
    print("Extracted Text: ")
    print(extracted_text)
    return extracted_text

def crop_lab(img_path):
    with Image.open(img_path) as img:
        width, height = img.size
        cropped_img = img.crop((0, (height*0.05), width, height))
    return cropped_img

def rng(df):
    # Set the seed for reproducibility
    np.random.seed(0)
    # Generate a random 9 digit number
    id = np.random.randint(100000000, 999999999)
    # Check if the ID is already in the df
    while id in df['random_ID'].values:
        id = np.random.randint(100000000, 999999999)
    return id

# Extract the student name and ID from the image
# To be replaced by file naming.
def extract_name(img_path, df):
    random_id = rng(df)
    cropped_img = crop_name(img_path, random_id)
    extracted_text = perform_ocr(cropped_img)
    # Find all sequences of letters in the text
    name = re.findall(r'[a-zA-Z]+', extracted_text)
    # Join the sequences into a single string
    name = ' '.join(name)
    # Find all sequences of numbers in the text
    numbers = re.findall(r'\d+', extracted_text)
    # Join the sequences into a single string
    numbers = ''.join(numbers)
    # Create a new DataFrame with the row to be added
    new_row = pd.DataFrame([{'Name': name, 'ID': numbers, 'random_ID': random_id}])
    # Concatenate the new row with the existing DataFrame
    df = pd.concat([df, new_row], ignore_index=True)
    return df, random_id


if __name__ == "__main__":
    img_path = "temp/12_1.png"
    df = pd.DataFrame(columns=['Name', 'ID', 'random_ID'])
    df, random_id = extract_name(img_path, df)
    io_utils.save_to_excel(df)