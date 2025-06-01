from django.shortcuts import render, HttpResponse,redirect
from django.http import HttpResponse, HttpResponseRedirect



def changeTheme(request,**kwargs):
    if 'is_dark_theme' in request.session:
        request.session['is_dark_theme'] = not request.session.get('is_dark_theme')
    else:
        request.session['is_dark_theme'] = True
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    # return redirect('index')  # Redirect to login page after logout
