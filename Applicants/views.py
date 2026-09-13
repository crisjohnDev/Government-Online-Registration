from django.shortcuts import render
from .models import Applicant

def new_registration(request):
    if request.method == "POST":
        