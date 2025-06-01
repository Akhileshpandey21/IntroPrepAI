from django.shortcuts import render, HttpResponse,redirect,HttpResponseRedirect,get_object_or_404
from django.http import HttpResponse, JsonResponse
from home.models import Contact
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import ImageUploadForm
from home.models import ImageUpload
from django.utils.translation import activate
from django.conf import settings
from dotenv import load_dotenv
import os
from django.core.files.storage import default_storage
from .utils import extract_resume_text
from .ai_helper import generate_interview_questions


from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .models import ChatMessage


from django.views.decorators.csrf import csrf_exempt
import json
from .chatbot import get_response

from django.contrib import messages


from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import time
import google.generativeai as genai


from .forms import ReviewForm
from .models import Review



from .utils import analyze_emotion, analyze_posture, analyze_sentiment
import cv2
import numpy as np
import base64

from django.http import FileResponse
from .pdf_generator import generate_interview_pdf


from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import render
from .models import Contact, ImageUpload


# Create your views here.


def index(request):
    latest_image = ImageUpload.objects.last()
    
    context={
        "variable":"Akhilesh Is a good boy he s "
    }
    reviews = Review.objects.all().order_by('-created_at')[:6]  # latest 6
    return render(request,"index.html",{"latest_image": latest_image,"reviews": reviews})
    # return HttpResponse("This is home page")


def about(request):
    latest_image = ImageUpload.objects.last()
    return render(request,"about.html",{"latest_image":latest_image})
    # return HttpResponse("This is about page")
def contact(request):
    latest_image = ImageUpload.objects.last()
    
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        
        # Save to database
        contact = Contact(
            firstName=first_name,
            lastName=last_name,
            email=email,
            phone=phone,
            message=message,
            created_at=timezone.now()
        )
        contact.save()

        # Send email
        subject = f"New Contact Message from {first_name} {last_name}"
        full_message = f"""
You have received a new message:

Name: {first_name} {last_name}
Email: {email}
Phone: {phone}
Message:
{message}
        """
        send_mail(
            subject,
            full_message,
            settings.DEFAULT_FROM_EMAIL,  # From
            [settings.CONTACT_RECEIVER_EMAIL],  # To
            fail_silently=False,
        )

        messages.success(request, 'Your message has been sent!')

    return render(request, "base.html", {"latest_image": latest_image})
    # return HttpResponse("This is contact page")

def services(request):
    latest_image = ImageUpload.objects.last()
    return render(request,"services.html",{"latest_image": latest_image})
    # return HttpResponse("This is services page")

def custom_404(request, exception):
    return render(request, '404.html', status=404)


# Login View
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "You have successfully logged in.")
            return redirect('/')  # Redirect to a dashboard or home page
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'login.html')

# Logout View
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('/')  # Redirect to login page after logout


@login_required
def dashboard(request):
    latest_image = ImageUpload.objects.last()
    return render(request, 'dashboard.html',{"latest_image": latest_image})


# Signup View
def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
            return redirect('signup')

        # Create user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        messages.success(request, "Signup successful! You can now log in.")
        return redirect('login')

    return render(request, 'signup.html')



# Image Upload View


def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Image uploaded successfully.")
            return redirect('dashboard')
    else:
        form = ImageUploadForm()
    return render(request, 'upload_image.html', {'form': form})



# bot view

def chatbot_page(request):
    return render(request, "chatbot.html")


@csrf_exempt
@login_required
def chatbot_response(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_input = data.get("message", "")

        bot_response = get_response(user_input)

        needs_admin = bot_response.lower() in ["I'm not sure about that. Let me connect you to an admin.".lower()]

        # Save the chat
        chat = ChatMessage.objects.create(user=request.user, user_message=user_input, bot_response=bot_response, needs_admin=needs_admin)
        chat.save()
        # Notify Admin if Needed
        if needs_admin:
            send_admin_alert(request.user, user_input)

        return JsonResponse({"response": bot_response, "needs_admin": needs_admin})

    return JsonResponse({"error": "Invalid request"}, status=400)

def send_admin_alert(user, user_message):
    """ Sends an email notification to the admin """
    admin_email = "admin@example.com"  # Change to your admin email
    subject = f"User {user.username} Needs Assistance!"
    message = f"User {user.username} asked: {user_message}\n\nPlease check the admin panel for more details."
    
    send_mail(subject, message, "no-reply@yourwebsite.com", [admin_email])



@login_required
def admin_respond(request):
    if request.method == "POST" and request.user.is_staff:
        data = json.loads(request.body)
        chat_id = data.get("chat_id")
        admin_response = data.get("response")

        chat = get_object_or_404(ChatMessage, id=chat_id)
        chat.bot_response = admin_response
        chat.needs_admin = False
        chat.save()

        return JsonResponse({"message": "Response saved successfully!"})

    return JsonResponse({"error": "Unauthorized"}, status=403)

# chat history
@login_required
def chat_history(request):
    chats = ChatMessage.objects.filter(user=request.user).order_by("-timestamp")[:10]  # Last 10 messages for logged-in user
    chat_data = [{"user_message": chat.user_message, "bot_response": chat.bot_response} for chat in chats]
    return JsonResponse({"history": chat_data})



def switch_language(request):
    lang = request.GET.get('lang', 'en')
    activate(lang)
    request.session[settings.LANGUAGE_COOKIE_NAME] = lang
    response = redirect(request.META.get('HTTP_REFERER', '/'))
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang)
    return response



# views for interview
load_dotenv()

# Configure Google Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
# model = genai.GenerativeModel("gemini-1.5-pro")
model = genai.GenerativeModel("gemini-2.0-flash")

# Store interview session data
interview_sessions = {}

def upload_resume(request):
    if request.method == "POST" and request.FILES.get("resume"):
        resume_file = request.FILES["resume"]
        job_title = request.POST.get("job_title")
        job_description = request.POST.get("job_description")

        file_path = default_storage.save(os.path.join("file_upload", resume_file.name), resume_file)

        
        resume_text = extract_resume_text(file_path)
       
        


      

        # Simulate processing time
        time.sleep(2)

        # Generate a fake session ID (replace with real session logic)
        session_id = "12345"


        
        # interview_questions = generate_interview_questions(job_title, job_description, resume_text)

        
        # return render(request, "results.html", {"questions": interview_questions})

    
        return JsonResponse({"session_id": session_id})

    return JsonResponse({"error": "Invalid request"}, status=400)


def interview_page(request, session_id):
    return render(request, "interview.html", {"session_id": session_id})

def form(request):
    return render(request,"form.html")


def result(request):
    return render(request,"results.html")





@login_required
@csrf_exempt
def start_interview(request):
    """ Start a new AI interview session """
    if request.method == "POST":
        data = json.loads(request.body)
        job_title = data.get("job_title")
        job_description = data.get("job_description")
        resume_text=data.get("resume_text")
        candidate_name = data.get("candidate_name")

        # Generate the first question
        prompt = f"Generate one interview question for a {job_title} based on this job description: {job_description} and Candiadate's resume: {resume_text}."
        response = model.generate_content(prompt)
        first_question = response.text
        # first_question = "What is your name ?"

        session_id = str(time.time())  # Unique session ID
        interview_sessions[session_id] = {
            "questions": [first_question],
            "answers": [],
            "start_time": time.time(),
        }

        return JsonResponse({"session_id": session_id, "question": first_question})

@csrf_exempt
def next_question(request):
    """ Handle user's answer and send the next question """
    if request.method == "POST":
        data = json.loads(request.body)
        session_id = data.get("session_id")
        user_answer = data.get("answer").strip().lower()

        if session_id not in interview_sessions:
            return JsonResponse({"error": "Invalid session"}, status=400)

        session = interview_sessions[session_id]
        session["answers"].append(user_answer)

        # Measure response time
        response_time = time.time() - session["start_time"]


           # If user explicitly says "stop the interview", evaluate immediately
        if user_answer in ["stop interview", "end interview", "finish interview"]:
            return evaluate_interview(request)

        # Check if maximum questions are reached (e.g., 5)
        if len(session["questions"]) >= 5:
            return evaluate_interview(request)


        # Generate the next question
        prompt = f"Based on this answer: '{user_answer}', generate the next interview question for the same job."
        response = model.generate_content(prompt)
        next_question = response.text

        # Store new question and update time
        session["questions"].append(next_question)
        session["start_time"] = time.time()

        return JsonResponse({"question": next_question, "response_time": response_time})

@csrf_exempt
def evaluate_interview(request):
    """ Evaluate candidate performance at the end """
    if request.method == "POST":
        data = json.loads(request.body)
        session_id = data.get("session_id")

        if session_id not in interview_sessions:
            return JsonResponse({"error": "Invalid session"}, status=400)

        session = interview_sessions[session_id]

        # Generate feedback based on all answers
        prompt = f"Evaluate this candidate based on their answers:\n\n{session['answers']}\n\nProvide a pass/fail decision and feedback."
        response = model.generate_content(prompt)
        
       

        # Delete session data after evaluation
        del interview_sessions[session_id]

        return JsonResponse({"result": response.text})


def submit_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for your review!")
            return redirect('/#testimonials?reviewed=true') # Redirect back to the same page
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = ReviewForm()
    return render(request, 'review_form.html', {'form': form})



def analyze_video_snapshot(request):
    """Accepts base64 webcam frame from JS and returns emotion/posture"""
    data = json.loads(request.body)
    answer = data.get("answer")
    img_data = data.get("frame")  # Base64 webcam image

    sentiment = analyze_sentiment(answer)

    emotion = posture = "Unknown"
    if img_data:
        img_bytes = base64.b64decode(img_data.split(',')[1])
        np_arr = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        emotion = analyze_emotion(frame)
        posture = analyze_posture(frame)

    return JsonResponse({
        "sentiment": sentiment,
        "emotion": emotion,
        "posture": posture
    })

def download_feedback_pdf(request):
    # Ideally this data is pulled from session/db
    candidate = request.POST.get("candidate_name")
    questions = request.POST.getlist("questions[]")
    answers = request.POST.getlist("answers[]")
    emotions = request.POST.getlist("emotions[]")
    postures = request.POST.getlist("postures[]")
    sentiments = request.POST.getlist("sentiments[]")

    filepath = "media/interview_report.pdf"
    generate_interview_pdf( filepath,
    candidate,
    questions,
    answers,
    emotions,
    postures,
    sentiments
    )

    return FileResponse(open(filepath, 'rb'), as_attachment=True, filename="AI_Interview_Feedback.pdf")

def video_interview(request):
    return render(request, "video_interview.html")

def analyze_answer(request):
    data = json.loads(request.body)
    answer = data.get("answer")

    # Dummy logic or your ML model
    emotion = analyze_emotion(answer)
    sentiment = analyze_sentiment(answer)
    posture = analyze_posture(answer)

    return JsonResponse({
        "emotion": emotion,
        "sentiment": sentiment,
        "posture": posture
    })


