import pandas as pd

def pdf2imagelist(download_dir, pdf):
    from pdf2image import convert_from_path
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

def read_excel_to_dataframe(file_path, sheet_name=0):
    # Read the Excel file into a DataFrame
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    return df

def save_mark(mark, df, random_id):
    # Save the mark to the DataFrame
    df.loc[df['random_ID'] == int(random_id), 'Grade'] = mark
    # print(df)
    # Save the updated DataFrame to an Excel file
    df.to_excel('data/student_data.xlsx', index=False)

def save_to_excel(df):
    # Save the df to an Excel file
    df.to_excel('data/student_data.xlsx', index=False)