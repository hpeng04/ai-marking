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