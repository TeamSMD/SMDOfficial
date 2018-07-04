from django.shortcuts import render, render_to_response

# Create your views here.

def index(request):
    return render(request, 'index.html')


def recent_activities(request):
    return render(request, 'recent_activities.html')


def research_paper(request):
    return render(request, 'SMD-ResearchPaper.html')


def contact_us(request):
    return render(request, 'contact_us.html')
