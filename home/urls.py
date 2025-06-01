from django.contrib import admin
from django.urls import path
from home import views

from django.urls import reverse_lazy

from django.contrib.auth import views as auth_views
from django.urls import path

urlpatterns = [
    path("",views.index,name="home"),
    path("about",views.about,name="about"),
    path("contact",views.contact,name="contact"),
    path("services",views.services,name="services"),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('signup/', views.signup_view, name='signup'),
    path('upload/', views.upload_image, name='upload_image'),

    path("chatbot/", views.chatbot_page, name="chatbot_page"),
    path('chatbot/api/', views.chatbot_response, name='chatbot_response'),
    path("chatbot/history/", views.chat_history, name="chat_history"),
    path("admin/respond/", views.admin_respond, name="admin_respond"),
    path('switch-language/', views.switch_language, name='switch_language'),

    path('upload-resume/', views.upload_resume, name="upload_resume"),

    path('result/', views.result, name="result"), # New URL which needs to be deleted
    path('start_interview/',views.start_interview,name="start_interview"),
    path('next_question/',views.next_question,name="next_question"),
    path('evaluate_interview/',views.evaluate_interview,name="evaluate_interview"),


    # path('interview-page/', views.interview_page, name='interview_page'),
    path('interview/<str:session_id>/', views.interview_page, name='interview_page'),
    path('form/', views.form, name='form'),


    path('submit-review/', views.submit_review, name='submit_review'),




    # dummy
    path('vedio_interview/', views.video_interview, name='video_interview'),
    path('analyze_answer/', views.analyze_answer, name='analyze_answer'),
    path('download_feedback_pdf/', views.download_feedback_pdf, name='download_feedback_pdf'),

    # Password reset URLs
    
# Your other URL patterns
     path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='password_reset.html',
        email_template_name='password_reset_email.html',
        subject_template_name='password_reset_subject.txt',
    ), name='password_reset'),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_done.html'
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm.html',
        success_url=reverse_lazy('login')  # 👈 redirects to login after reset
    ), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset_done.html'
    ), name='password_reset_complete'),
]
