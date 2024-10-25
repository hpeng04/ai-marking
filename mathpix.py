import requests
import json
import ocr_utils
import io
from PIL import Image

def getheaders():
    with open("secrets/mathpix_api_key", "r") as key_file:
        api_key = key_file.read().strip()

    with open("secrets/mathpix_app_id", "r") as id_file:
        app_id = id_file.read().strip()

    return {
        "app_id": f"{app_id}",
        "app_key": f"{api_key}"
    }

def process(image_path):
    headers = getheaders()

    with Image.open(image_path) as img:
        img = ocr_utils.preprocess_image(img)
        # Convert the PIL image to a BytesIO object
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)

    r = requests.post("https://api.mathpix.com/v3/text",
        files={"file": ("image.png", img_byte_arr, "image/png")},
        data={
        "options_json": json.dumps({
            "math_inline_delimiters": ["$", "$"],
            "rm_spaces": True
        })
        },
        headers=headers
    )
    # try:
    return r.json().get('text')
    # except KeyError:
    #     return ""
    
if __name__ == "__main__":
    image_path = "temp/309652396_1.png"
    pdf_id = process(image_path)
    print(pdf_id)
