from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.http import HttpResponse

# Create your views here.
def redirector(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/home')
    else:
        return redirect('/login')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        next_path = request.POST.get('next')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            if next_path == "None":
                return redirect('/dashboard/home')
            else:
                return redirect(next_path)
        else:
            messages.info(request, "invalid credentials")
            return redirect('/')    
    else:
        return render(request, 'login.html', {'next': request.GET.get('next')})


def logout(request):
    auth.logout(request)
    return HttpResponse('''
    <h3>You have succesfully logged out!</h3>
    <br>
    <button onclick="location.href='/'">Login Again?</button>
    ''')