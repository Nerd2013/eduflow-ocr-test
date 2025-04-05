
import streamlit as st
from PIL import Image, ImageDraw
import pytesseract
import os

st.title("EduFlow: Bulk MCQ Scanner")

pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

def extract_student_name(img):
    width, height = img.size
    cropped = img.crop((0, 0, width, int(height * 0.1)))
    text = pytesseract.image_to_string(cropped)
    return text.strip().split("\n")[0] if text.strip() else "Unknown"

def highlight_results(image, answers, answer_key):
    draw = ImageDraw.Draw(image)
    for q_num, student_ans in answers.items():
        x, y = 50 + int(q_num) * 20, 100  # Fake positions for now
        correct = answer_key.get(q_num) == student_ans
        color = "green" if correct else "red"
        if correct:
            draw.ellipse([x-10, y-10, x+10, y+10], outline=color, width=3)
        else:
            draw.line([x-10, y-10, x+10, y+10], fill=color, width=3)
            draw.line([x-10, y+10, x+10, y-10], fill=color, width=3)
    return image

def dummy_detect_answers(img):
    return {"1": "A", "2": "B", "3": "C"}  # Placeholder for bubble detection

st.header("Step 1: Upload Answer Key Sheet")
key_file = st.file_uploader("Upload teacher answer sheet", type=["jpg", "png", "jpeg"], key="key")
answer_key = {}

if key_file:
    key_img = Image.open(key_file)
    answer_key = dummy_detect_answers(key_img)
    st.success("Answer key detected (simulated):")
    st.json(answer_key)

st.header("Step 2: Upload Student Answer Sheets")
student_files = st.file_uploader("Upload student sheets", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

if student_files and answer_key:
    for student_file in student_files:
        img = Image.open(student_file)
        name = extract_student_name(img)
        answers = dummy_detect_answers(img)
        annotated = highlight_results(img, answers, answer_key)
        st.subheader(f"Student: {name}")
        st.image(annotated, use_column_width=True)
        st.write("Detected Answers:", answers)
