from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib import messages

# Create your views here.
def index(request):
    # Render index.html
    return render( request, 'aintdoinit/index.html')

def toggle_dark_mode(request):
    current_mode = request.session.get('dark_mode', False)
    print("Current dark mode status:", current_mode)  # Debug line
    request.session['dark_mode'] = not current_mode
    return redirect(request.META.get('HTTP_REFERER', 'default_url_if_no_referer'))