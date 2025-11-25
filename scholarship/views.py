from django.shortcuts import render

# Create your views here.
def scholarship_index(request):
    return render(request, 'scholarship_index.html')