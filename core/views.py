from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from files.forms import DocumentForm
from django.urls import reverse
from django.views import generic
from files.models import FileObject
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from core.forms import SignUpForm
from django.contrib import messages

@login_required
def home(request):
	return render(request, 'core/home.html')

@login_required
def model_form_upload(request):
	if request.method == 'POST':
		form = DocumentForm(request.POST, request.FILES)
		if form.is_valid():
			doc = form.save(commit=False)
			doc.user = request.user
			doc.save()
			messages.success(request, 'File successfully uploaded!')
			return HttpResponseRedirect(reverse('home'))
	else:
		form = DocumentForm()
	return render(request, 'core/model_form_upload.html', {
		'form': form
	})

@login_required
def my_files(request):
	query_results = FileObject.objects.filter(user=request.user)
	return render(request, 'core/my_files.html', {'query_results':query_results})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'core/signup.html', {'form': form})