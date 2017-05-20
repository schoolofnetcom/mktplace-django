from django.shortcuts import render, render_to_response


def home(request):
    return render(request, 'portal/home.html',{})