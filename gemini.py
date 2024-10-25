import pathlib
import textwrap
import PIL

import google.generativeai as genai

# DEPRECATED
def digitize(image_path):
    # with open("./secrets/gpt_api_key", "r") as key_file:
    #     GOOGLE_API_KEY = key_file.read().strip()
    GOOGLE_API_KEY = r"AIzaSyARsvUj219BxrE0eyf7saWqxDBXy_uKz3o"

    model = genai.GenerativeModel('models/gemini-1.5-pro-latest')

    img = PIL.Image.open(image_path)

    genai.configure(api_key=GOOGLE_API_KEY)

    response = model.generate_content(
        [
    "Task: Extract everything that is asked to be calculated in the question from the attached image. This includes not only the variables but also any intermediate steps, formulas, or values that are necessary to solve the problem. The images contain the handwritten solutions to one or more questions, and you need to extract all the information relevant to each question's solution. The questions are summarized below. Make sure to capture all parts of the solution for each question, including any intermediate steps:"

    "For Question 1, calculate the x, y, and z scalar components of vector F, express F in Cartesian vector form, determine the direction angles α, β, and γ of force F with respect to the x, y, and z axes, and verify that the direction angles satisfy the requirement cos² α + cos² β + cos² γ = 1. Then, express F as a product of its magnitude and directional unit vector, for example, {10(0.1i + 0.2j + 0.3k)} N."

    "For Question 2, determine the magnitude and direction angles of F3 shown in Figure 2, so that the resultant of the three forces is zero."

    "For Question 3, involving two cables AB and AC acting on a hook at point A as shown in Figure 3, determine the position vectors for the internal forces labeled FB and FC, express forces FB and FC in Cartesian vector form, determine the resultant force R in Cartesian vector form along with its magnitude and direction angles, and find the angle at point A formed by cables AB and AC."

    "Ensure that you extract all calculations, intermediate steps, and final results as they appear in the handwritten solution. Some images may contain solutions for only one question, while others may contain solution of two questions. Image:", img
        ],

        stream=True
    )
    response.resolve()
    return response.text

def mark_lab(solution_path, student_work_path):
    with open("secrets/gemini_api_key", "r") as key_file:
        api_key = key_file.read().strip()

    with open("prompts/marking_prompt.txt", "r", encoding='utf-8') as prompt_file:
        rubric = prompt_file.read()
    
    with open(solution_path, "r", encoding='ISO-8859-1') as solution_file:
        solution = solution_file.read()

    with open(student_work_path, "r", encoding='ISO-8859-1') as student_work_file:
        student_work = student_work_file.read()

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel('models/gemini-1.5-pro-latest')

    # Prepare a task prompt for the model
    task_prompt = f"""
    Task: Evaluate the student's answer based on the provided rubric and the standard solution. 
    For each question, compare the student's answer to the standard solution and assign a mark based on the rubric. 
    Provide a brief feedback and justification for each question.

    Rubric: {rubric}

    Standard Solution: {solution}

    Student's Answer: {student_work}

    Write the total score as a single integer value at the last line.
    """

    # Perform the evaluation by passing the task prompt to the model
    response = model.generate_content([task_prompt], stream=True)
    response.resolve()

    return response.text

if __name__ == "__main__":
    TEMP_PATH = r"temp/309652396_1.png"
    text = digitize(TEMP_PATH)
    print(text)
    