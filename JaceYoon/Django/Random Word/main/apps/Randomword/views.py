from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string
import random

# Create your views here.
def index(request):
    if not 'num' in request.session:
        request.session['num'] = 0
    return render(request,'Randomword/index.html')

def random(request):
    print(request.method)
    if request.method == "POST":
        request.session['num'] += 1
        unique_id = get_random_string(length=14)
        request.session['random'] = unique_id
        print (request.POST)
        return redirect('/')
    else:
        return redirect('/')

def reset(request):
    del request.session['num']
    del request.session['random']
    return redirect('/')
