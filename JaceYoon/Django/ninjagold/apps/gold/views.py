from django.shortcuts import render, redirect
import random,time

# Create your views here.
def index(request):
    if not 'total' in request.session:
        request.session['total'] = 0
    if not 'act' in request.session:
        request.session['act'] = []
    return render(request,"gold/game.html")

def run(request):
    places = {
        "farm" : random.randrange(10,20),
        "cave" : random.randrange(5,10),
        "house" : random.randrange(2,5),
        "casino" : random.randrange(-50,50)
        }
    if request.POST["building"] in places:
        renew = places[request.POST["building"]]
        request.session['total'] += renew
        text = {
            "class" : "green" if renew > 0 else "red" ,
            "activity" : "You went {} and {} {} golds".format(request.POST['building'],('lose','earn')[renew >0], renew),
            "clock" : " (" + time.strftime("%Y/%m/%d") + " " + time.strftime("%I:%M %p") + ")"
        }
        request.session['act'].append(text)

        return redirect('/')

def reset(request):
    request.session['total'] = 0
    request.session['act'] = []
    return redirect('/')
# bolean [ jace, ian ] true = "ian " false = "jace"
