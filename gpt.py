from openai import OpenAI
import os
import base64
import requests

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def digitize_student_work(image_path):
    # OpenAI GPT API Key
    with open("secrets/gpt_api_key", "r") as key_file:
        api_key = key_file.read().strip()

    with open("prompts/digitize_student_work.txt", "r") as prompt_file:
        prompt = prompt_file.read()

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
            """
        },
        {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": prompt
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

    return response.json()['choices'][0]['message']['content']

def digitize_solution(image_path):
    # OpenAI GPT API Key
    with open("secrets/gpt_api_key", "r") as key_file:
        api_key = key_file.read().strip()

    with open("prompts/digitize_solution.txt", "r") as prompt_file:
        prompt = prompt_file.read()

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
            "content": prompt
        },
        {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": """Perform OCR on the given image and extract the diagrams in the image by
                        describing the force vectors."""
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

    return response.json()['choices'][0]['message']['content']

def mark_lab(solution_path, student_work_path):
    # OpenAI GPT API Key
    with open("secrets/gpt_api_key", "r") as key_file:
        api_key = key_file.read().strip()

    with open("prompts/marking_prompt.txt", "r", encoding='utf-8') as prompt_file:
        prompt = prompt_file.read()
    
    with open(solution_path, "r", encoding='ISO-8859-1') as solution_file:
        solution = solution_file.read()

    with open(student_work_path, "r", encoding='ISO-8859-1') as student_work_file:
        student_work = student_work_file.read()

    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
    }

    payload = {
    "model": "gpt-4o-mini",
    "messages": [
        {
            "role": "system",
            "content": prompt
        },
        # {
        #     "role": "user",
        #     "content": [
        #         {
        #         "type": "text",
        #         "text": f"Solution: {solution} This is the correct solution. Reference this when marking the student solution given below."
        #         }
        #     ]
        # },
        {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": f'''Solution: {solution} This is the correct solution. Reference this when marking the student solution given below.
                        Student Work: {student_work} Give the total mark assignment score including points for all questions as
                        a simple single integer value. eg. If the final score is 10 out of 15, then write 10 in the last line.'''
                }
            ]
        },
        {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": """Mark the student's work based on the solution and marking scheme provided."""
                }
            ]
        }
    ],
    "max_tokens": 3000
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    return response.json()['choices'][0]['message']['content']