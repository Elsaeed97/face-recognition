from django.shortcuts import render,redirect
from .forms import UserRegistrationForm , LoginForm
from django.contrib import auth
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from .models import Profile
import os 
from django.urls import path, include
import face_recognition
import cv2 
from django.http import HttpResponse 
# Create your views here.

def index(request):
	return render(request,'index.html')

def register(request):
	if request.method == 'POST':
		user_form = UserRegistrationForm(request.POST)
		if user_form.is_valid():
			new_user = user_form.save(commit=False)
			new_user.set_password(user_form.cleaned_data['password'])
			new_user.save()
			return render(request,'account/register_done.html',{'new_user':new_user})
	else:
		user_form = UserRegistrationForm()
	return render(request,'account/register.html',{'user_form':user_form})

def facedect(loc):
	cam = cv2.VideoCapture(0)   
	s, img = cam.read()
	if s:                  
		BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		MEDIA_ROOT =os.path.join(BASE_DIR,'')

		loc=(str(MEDIA_ROOT)+loc)
		print(loc)
		face_1_image = face_recognition.load_image_file(loc)
		face_1_face_encoding = face_recognition.face_encodings(face_1_image)[0]
		small_frame = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
		rgb_small_frame = small_frame[:, :, ::-1]

		face_locations = face_recognition.face_locations(rgb_small_frame)
		face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

		check=face_recognition.compare_faces(face_1_face_encoding, face_encodings)                
		print(check)
		if check[0]:
			return True

		else:
			return False  


def login_user(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request,username=username,password=password)
		profile = Profile()
		if user is not None:
			# prof = user.profile.photo.url
			# print(prof)
			if facedect(user.profile.photo.url):
				login(request, user)
				return redirect('index')
			else:
				return redirect('login')
		else:
			return redirect('login')
	else:
		form = LoginForm()
		return render(request, 'account/login.html', {'form':form})

		


def profile(request):
	return render(request,'account/profile.html')
