from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required(login_url='login')
def index(request):
    return render(request, 'home/home.html', {})
