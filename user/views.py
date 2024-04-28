from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from .models import City,Data,Profile,Jobs,Tag,Post
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate, logout, login
from django.db.models import Q # new
from .forms import  ProfileForm, UserForm,PostForm
from django.template.loader import render_to_string
from django.conf import settings
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import get_object_or_404, redirect, render


def home(request):
    model = Post    

    post = Post.objects.all()
    context = {
        'post': post
    }

    return render(request, 'users/home.html' ,context)

def about(request):
    return render(request, 'users/about.html')


def postjob(request):

    return render(request, 'users/post-job.html')


@login_required
def job_detail(request):

    model = Post    
    post = Post.objects.all()

    context = {
        'post': post
    }
    return render(request, 'users/job-detail.html' , context )

@csrf_protect
@login_required(login_url="home")
def createPost(request):
	form = PostForm()

	if request.method == 'POST':
		form = PostForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
		return redirect('job-list')
	context = {'form':form}
	return render(request, 'users/post_form.html', context)


@login_required
def job_list(request):

    model = Post
    def get_queryset(self): # new
        return Post.objects.filter(
            Q(cname__icontains="q") | Q(l__icontains="q")
        )

    if 'q' in request.GET:
        q = request.GET['q']
        post = Post.objects.filter(cname__icontains=q)
        post = Post.objects.filter(lname__icontains=q)
        multiple_q = q(q(cname__icontains=q)|q(lname__icontains=q))
        post = Post.objects.filter(q)
    else:
        post = Post.objects.all()
    context = {
        'post': post
    }
    return render(request, 'users/job-list.html' , context )
   
    
def contact(request, post_id):
    
    model = Post
    post = get_object_or_404(Post, pk=post_id)

    return render(request, 'users/contact.html', {'post': post})

@login_required
def category(request):
    model = Jobs

    if 'q' in request.GET:
        q = request.GET['q']
        jobs = Jobs.objects.filter(cname__icontains='q')
    jobs = Jobs.objects.all()
    context = {
        'jobs': jobs
    }
    return render(request, 'users/category.html', context)

def testimonial(request):
    return render(request, 'users/testimonial.html')

def navbar(request):
    return render(request, 'users/navbar.html')

def profile(request):

    return render(request, 'users/profile.html')

@login_required
def logout(request):
    logout(request)

    messages.success(request, "Logged Out Successfully!!")

    return redirect('/')

########################################################################
########### register here #####################################

def registration(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST) or None
        if form.is_valid():
            username = request.POST.get('username')
            #########################mail####################################
            htmly = get_template('users/email.html')
            d = { 'username': username }
            subject, from_email, to = 'hello', 'from@example.com', 'to@emaple.com'
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            try:
                msg.send()
            except:
                print("error in sending mail")
            ##################################################################
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/registration.html', {'form': form})

###################################################################################
################login forms###################################################
@csrf_protect
def Login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
    
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.info(request, f"You are now logged in as {username}.")
            return redirect('/')
        else:
            messages.error(request,"Invalid username or password.")
    
    form = AuthenticationForm(request, data=request.POST)
    return render(request, 'users/login.html', {'form':form})

@login_required(login_url="home")
def updateProfile(request):
	user = request.user
	profile = user.profile
	form = ProfileForm(instance=profile)
	if request.method == 'POST':
		user_form = UserForm(request.POST, instance=user)
		if user_form.is_valid():
			user_form.save()
		form = ProfileForm(request.POST, instance=profile)
		if form.is_valid():
			form.save()
			return redirect('profile')
	context = {'form':form}
	return render(request, 'users/profile_update.html', context)

def sendEmail(request):
	if request.method == 'POST':
		template = render_to_string('users/email_template.html', {
			'name':request.POST['name'],
			'email':request.POST['email'],
			'message':request.POST['message'],
			})
		email = EmailMessage(
			request.POST['subject'],
			template,
			settings.EMAIL_HOST_USER,
			['plugrapher@gmail.com']
			)
		email.fail_silently=False
		email.send()
	return render(request, 'users/email_sent.html')


def post(request):
	post = Post.objects.get()

	if request.method == 'POST':

		return redirect('job-list')


	context = {'post':post}
	return render(request, 'users/post.html',context)


@login_required(login_url="home")
def updatePost(request):
	post = Post.objects.get()
	form = PostForm(instance=post)

	if request.method == 'POST':
		form = PostForm(request.POST, instance=post)
		if form.is_valid():
			form.save()
		return redirect('job-detail')
	context = {'form':form}
	return render(request, 'users/post_form.html', context)

@login_required(login_url="home")
def deletePost(request, post_id):
    post = Post.objects.get(pk=post_id)  # Retrieve the post object

    if request.method == 'POST':
        post.delete()
        return redirect('job-list')
    context = {'post':post}
    return render(request, 'users/delete.html', context)

