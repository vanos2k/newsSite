from django.shortcuts import render, redirect
from django.contrib.auth import logout
from News.views import index
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate


def logout_view(request):
    logout(request)
    return redirect(index)


def registration_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('main_url')
    else:
        form = UserCreationForm()
    return render(request, 'registration/registration.html', {'form': form})
