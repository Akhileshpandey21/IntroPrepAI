import os
import pdfplumber
import docx2txt
from django.core.files.storage import default_storage

import cv2
from fer import FER
import mediapipe as mp
import numpy as np

from textblob import TextBlob

def extract_resume_text(resume_path):
    """Extract text from PDF or DOCX resumes"""
    resume_path = default_storage.path(resume_path)  # Get the full path
    _, ext = os.path.splitext(resume_path)
    ext = ext.lower()  # Make it case-insensitive

    try:
        if ext == ".pdf":
            with pdfplumber.open(resume_path) as pdf:
                text = "".join([page.extract_text() or "" for page in pdf.pages])
        elif ext == ".docx":
            text = docx2txt.process(resume_path)
        else:
            text = "Unsupported file format"
    except Exception as e:
        text = f"Error reading file: {str(e)}"

    return text.strip()



# Initialize emotion detector
emotion_detector = FER(mtcnn=True)

# Initialize posture detector
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

def analyze_emotion(frame):
    """Returns top emotion from a face in frame."""
    try:
        result = emotion_detector.top_emotion(frame)
        return result[0] if result else "Neutral"
    except Exception:
        return "Neutral"

def analyze_posture(frame):
    """Detects if user is slouched or upright."""
    try:
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb_frame)

        if not results.pose_landmarks:
            return "Unknown"

        left_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
        right_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]

        shoulder_y_diff = abs(left_shoulder.y - right_shoulder.y)
        if shoulder_y_diff > 0.05:
            return "Slouched"
        return "Straight"

    except Exception:
        return "Unknown"



def analyze_sentiment(text):
    """
    Analyzes sentiment of the given text.
    Returns: 'Positive', 'Neutral', or 'Negative'
    """
    if not text.strip():
        return "Neutral"

    blob = TextBlob(text)
    polarity = blob.sentiment.polarity  # [-1.0, 1.0]

    if polarity > 0.2:
        return "Positive"
    elif polarity < -0.2:
        return "Negative"
    else:
        return "Neutral"
