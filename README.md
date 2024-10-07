### Action Plan:

### 1. **Accessing PDF Files:**

- The script will access a specified directory where the students’ PDF files are stored.
- It will iterate through each PDF file, reading them one by one.
- Each PDF will be converted into images (one image per page).

### 2. **Digitizing Content:**

- The script will send the images to the script written by "Mohammad Aqib" to extract the text from the images.
- A "digitization" prompt file, already saved in the source folder, contains instructions for digitizing the images. This prompt file will be opened and read before processing.
- The extracted text for each PDF will be saved in a separate folder (e.g., "Digitized_Texts") with the same name as the original PDF.

### 3. **Using Marking Prompts:**

- The script will read marking prompts from a specific folder.
- It will then pass the digitized text to another script (to be written) that uses ChatGPT to evaluate whether the solutions are correct step by step.
- For each student, feedback will be generated and saved in a new folder (e.g., "Feedbacks") under the student's name, followed by "-feedback" as a text file.

### 4. **Grading and Final Output:**

- Based on the comparison between the student's digitized text and the correct solution, the final grade will be calculated.
- The grade will be recorded in an Excel sheet, where the PDF file name and corresponding grade will be listed.

### 5. **Processing the Correct Solutions First:**

- Before processing student submissions, the correct solution PDFs will be handled similarly (reading, digitizing, and saving).
- These correct solutions will be used as a benchmark for grading students' answers by combining them with the marking prompts and ChatGPT.

### 6. **Iterating Through Students:**

- After completing the evaluation for one student, the system will proceed to the next student.
- This loop continues until all students’ submissions are processed and graded.

---

### Workflow Summary:

- **Input Folders:**
    - PDFs of student submissions
    - Correct solution PDFs
    - Text file with digitization prompts
    - Folder with marking prompts
- **Output:**
    - Digitized text files for each student
    - Feedback files with ChatGPT evaluations
    - Final grade recorded in an Excel sheet