from django.http  import HttpResponse,Http404
import datetime as dt
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import *
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User


# Create your views here.

# app view functions
def index(request):
    date = dt.date.today()
    hoods = Neighbourhood.objects.all()
    form = HoodForm(request.POST,instance = request.user.profile.neighbourhood)
    return render(request, 'landing.html',{"date":date, "hoods":hoods,"form":form})

def profile(request):
    date = dt.date.today()
    current_user = request.user
    hoods = Neighbourhood.objects.all()
    profile = Profile.objects.filter(profile=current_user)

    if len(profile)<1:
        profile = "No profile"
    else:
        profile = Profile.objects.get(profile=current_user)

    return render(request, 'profile/profile.html', {"date": date, "profile":profile,"hoods":hoods})
@login_required
def edit_profile(request):
    date = dt.date.today()
    current_user = request.user
    if request.method == 'POST':
        signup_form = EditForm(request.POST, request.FILES,instance=request.user.profile)
        if signup_form.is_valid():
            signup_form.save()
            return redirect('profile')
    else:
        signup_form =EditForm(instance = request.user.profile)

    return render(request, 'profile/edit_profile.html', {"date": date, "form":signup_form,"profile":profile})

@login_required(login_url='/accounts/login/')
def new_hood(request):
    current_user = request.user
    if request.method == 'POST':
        form = HoodForm(request.POST, request.FILES)
        if form.is_valid():
            hood = form.save(commit=False)
            hood.user = current_user
            hood.profile = profile
            hood.save()
        return redirect('index')
    else:
        form = HoodForm()
    return render(request, 'new_hood.html', {"form": form})

@login_required(login_url='/accounts/login/')
def search_results(request):
    if 'business' in request.GET and request.GET["business"]:
        search_term = request.GET.get("business")
        searched_businesses = Business.objects.filter(name=search_term)
        message = f"{search_term}"
        profiles=  Profile.objects.all( )

        return render(request, 'search.html',{"message":message,"business": searched_businesses,'profiles':profiles})

    else:
        message = "You haven't searched for any term"
        return render(request, 'search.html',{"message":message})


def location(request):
    date = dt.date.today()
    return render(request, 'location.html',{"date":date})

@login_required(login_url='/accounts/login/')
def hoods(request,id):
    current_user=request.user
    date = dt.date.today()
    post=Neighbourhood.objects.get(id=id)
    if request.method == 'POST':
        form = NewReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.judge = request.user.profile
            review.neighbourhood = hood
            review.save()
            return redirect('index')
    else:
        form = BusinessForm()
    brushs = Post.objects.filter(neighbourhood=post)
    business = Business.objects.filter(neighbourhood=post)
    return render(request,'neighoodlist.html',{"post":post,"date":date,"brushs":brushs, "business":business})



def new_business(request,id):
    date = dt.date.today()
    hood=Neighbourhood.objects.get(id=id)
    business = Business.objects.filter(neighbourhood=hood)
    form = BusinessForm()
    if request.method == 'POST':
        form = BusinessForm(request.POST, request.FILES)
        if form.is_valid():
            business = form.save(commit=False)
            business.profile = request.user.profile
            business.neighbourhood = hood
            business.save()
            return render(request,'new_business.html')
    else:
        form = BusinessForm()
        return render(request,'new_business.html',{"form":form,"business":business,"hood":hood,  "date":date})

def new_post(request,id):
    date = dt.date.today()
    hood=Neighbourhood.objects.get(id=id)
    posts = Post.objects.filter(neighbourhood=hood)
    comments = Comment.objects.filter(post=id).order_by('-pub_date')

    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user.profile
            post.profile = profile
            post.neighbourhood = hood
            post.save()
            return redirect('index')
    else:
        form = PostForm()
        return render(request,'new_post.html',{"form":form,"posts":posts,"hood":hood,  "date":date, 'comments':comments})

def newcomment(request,id):
    current_user = request.user

    try:
        comments = Comment.objects.filter(post_id=id)
    except:
        comments = []
    brush= Post.objects.get(id=id)
    if request.method =="POST":
        form = NewCommentForm(request.POST,request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.postername = current_user
            comment.post = brush
            comment.save()
    else:
        form = NewCommentForm()

    return render(request, 'newcomment.html',{'brush':brush,"comments":comments,"form":form})
