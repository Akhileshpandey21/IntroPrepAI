import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_interview_questions(job_title, job_description, resume_text):
    prompt = f"""
    You are an AI interviewer. Based on the job title: '{job_title}', job description: '{job_description}', 
    and the candidate's resume: '{resume_text}', generate 5 relevant interview questions.
    """
    
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    
    return response.text.strip().split("\n")
