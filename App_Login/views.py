from django.shortcuts import render,HttpResponseRedirect
from .forms import CreateNewUser,LogInUser,EditProfile
from django.contrib.auth.decorators import login_required
from django.urls import reverse,reverse_lazy
from django.contrib.auth import login,logout,authenticate
from.models import UserProfile,Follow
from django.contrib.auth.forms import AuthenticationForm
from App_Post.forms import PostForm
from django.contrib.auth.models import User

# Create your views here.


def sign_up(request):
    form = CreateNewUser()
    registered = False
    if request.method == 'POST':
        form = CreateNewUser(data=request.POST)
        if form.is_valid():
            form.save()
            registered = True
           
            return HttpResponseRedirect(reverse('App_Login:login'))
    return render(request, 'App_Login/signup.html', context={'title':'Sign up | TanvirGRam', 'form':form})



def Login_page(request):
    form = LogInUser()
    if request.method == 'POST':
        form = LogInUser(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request,user)
                return HttpResponseRedirect(reverse('App_Post:home'))
    return render(request,'App_Login/login.html',context={'title':'Login | TanvirGRam','form':form})



@login_required
def edit_profile(request):
    current_user = UserProfile.objects.get(user=request.user)
    form = EditProfile(instance=current_user)
    if request.method == 'POST':
        form = EditProfile(request.POST, request.FILES, instance=current_user)
        if form.is_valid():
            form.save(commit=True)
            form = EditProfile(instance=current_user)
            return HttpResponseRedirect(reverse('App_Login:profile'))
    return render(request, 'App_Login/profile.html', context={'form':form, 'title':'Edit Profile | TanvirGram'})

@login_required

def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('App_Login:login'))

@login_required
def profile(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return HttpResponseRedirect(reverse('App_Post:home'))
    return render(request, 'App_Login/user.html', context={'title':'User Profile | TanvirGRam','form': form})

@login_required

def user(request,username):
    user_other = User.objects.get(username=username)
    already_followed = Follow.objects.filter(follower = request.user, following=user_other)
    if user_other == request.user:
        return HttpResponseRedirect(reverse('App_Login:profile'))

    return render(request, 'App_Login/user_other.html',context={'user_other':user_other,'already_followed':already_followed})


@login_required

def follow(request,username):
    following_user = User.objects.get(username = username)
    follower_user = request.user
    already_followed = Follow.objects.filter(follower = follower_user,following = following_user)

    if not already_followed:
        followed_user = Follow(follower = follower_user,following = following_user)
        followed_user.save()
    return HttpResponseRedirect(reverse('App_Login:user',kwargs={'username':username}))


def unfollow(request,username):
    following_user = User.objects.get(username=username)
    follower_user = request.user
    already_followed = Follow.objects.filter(follower = follower_user,following=following_user)
    already_followed.delete()
    return HttpResponseRedirect(reverse('App_Login:user',kwargs={'username':username}))


