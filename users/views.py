from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm

# Create your views here.

def register(request):
    if request.method=='POST':
        form=UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            messages.success(request,f'Your account has been created! Please login')
            return redirect('login')
        else:
            messages.error(request,f'Something was wrong, please try again')
            return redirect('register')
    else:
        form=UserRegisterForm()
    return render(request,'users/register.html',{'form':form})

