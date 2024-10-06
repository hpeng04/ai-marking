from openai import OpenAI
import os
import base64
import requests

### WIP ###

def process(image_path):
    # OpenAI GPT API Key
    with open("./secrets/gpt_api_key", "r") as key_file:
        api_key = key_file.read().strip()

    # Function to encode the image
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    # Getting the base64 string
    base64_image = encode_image(image_path)

    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
    }

    payload = {
    "model": "gpt-4o-mini",
    "messages": [
        {
            "role": "system",
            "content": """You are an engineering assistant tasked with analyzing force vector diagrams and calculations. 
            Answer in plain text without markup or LaTeX. Analyze angles counter clockwise from the positive x-axis or an appropriate reference axis.
            Angles may be represented by variables on the diagram; analyze the calculations to find the angles.
            If there are no drawings/diagrams present, then respond "N/A"
            Answer in the following format:
            Figure {{#}}:
            {{variable}}: ###N, ###°
            {{variable}}: ###N, ###° 
            Separate each figure."""
        },
        {
            "role": "user",
            "content": [
                {
                "type": "text",
                # "text": """Digitalize the diagrams in the image."""
                "text": """Digitalize the student's **drawings** and **graphs** by extracting vectors, magnitudes, angles and analyzing relevant calculations. 
                        Include every force vectors in each diagram.

                        Describe all the details you see in the figure. 
                        """
                },
                {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}",
                    "detail": "high"
                }
                }
            ]
        }
    ],
    "max_tokens": 3000
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    content = eval(str(response.json()))
    with open(f"{image_path}.txt", "w") as result:
        # result.write(str(response.json()))
        result.write(str(content['choices'][0]['message']['content']))

    return response.json()
