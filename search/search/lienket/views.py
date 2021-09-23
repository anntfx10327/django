from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "lienket/index.html")

def image(request):
    return render(request, "lienket/image.html")

def advanced(request):
    return render(request, "lienket/advanced.html")