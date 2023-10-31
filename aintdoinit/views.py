from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib import messages

# Create your views here.
def index(request):
    # Render index.html
    return render( request, 'aintdoinit/index.html')

def toggle_dark_mode(request):
    # If the dark_mode flag exists and is True, set it to False. Otherwise, set it to True.
    request.session['dark_mode'] = not request.session.get('dark_mode', False)
    return redirect(request.META.get('HTTP_REFERER', 'default_url_if_no_referer'))