from django.shortcuts import render,redirect
from .forms import SignupForm, EditInfoForm, PasswordForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

# Create your views here.

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request,'signup.html')

def normalSignupForm(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user:login')
        else:
            print(form.errors)
    else :
        form = SignupForm()
    return render(request, 'normalSignupForm.html',{'form':form})  

def enterpriseSignupForm(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user:login')
        else:
            print(form.errors)
    else :
        form = SignupForm()
    return render(request, 'enterpriseSignupForm.html',{'form':form})  

@login_required
def myPage(request):
    return render(request, 'myPage.html')
    
@login_required 
def editInfo(request):
    user = request.user

    if request.method == 'POST':
        form = EditInfoForm(request.POST, instance=user)
        pwForm = PasswordForm(user=request.user,data=request.POST)
        is_change_password = bool(int(request.POST["is_change_password"]))
        if form.is_valid():
            form.save()
            if is_change_password:
                if pwForm.is_valid():
                    pwForm.save()
                    update_session_auth_hash(request, user)
                    return redirect('user:myPage') 
            else :
                return redirect('user:myPage') 
        else:
            print(form.errors) 
    else:
        form = EditInfoForm(instance=user)
        pwForm = PasswordForm(request.user)

    return render(request, 'editInfo.html', {'form': form, 'pwForm':pwForm})

@login_required
def editPw(request):
    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('user:login')
    else:
        form = PasswordForm(request.user)
    return render(request, 'editPw.html', {'form': form})
    