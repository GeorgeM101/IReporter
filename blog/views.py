from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, HttpResponse, redirect
from .forms import Video_form
from .models import Video


# def home(request):
#     context = {
#         'posts': Post.objects.all()
#     }
#     return render(request, 'blog/home.html', context)


# def base(request):
#     return render(request, 'blog/base.html')

def about(request):
    return render(request, 'blog/about.html', {'title': "About Page"})


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ["-date_posted"]


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # def test_func(self):
    #     post = self.get_object()
    #     if self.request.user == post.author:
    #         return True
    #     return False


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

# Video upload section


def video(request):
    form = Video_form()
    all_video = Video.objects.all()
    if request.method == "POST":
        form = Video_form(data=request.POST, files=request.FILES)
    if form.is_valid():
        form.save()
        return HttpResponse("<h1> Uploaded successfully </h1>")
    else:
        form = Video_form()
    return render(request, 'blog/videos.html', {"form": form, "all": all_video})



from multiprocessing import context
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import red_flag,Category,UserProfile,invention_records,Location,Contact,Post
import cloudinary
import cloudinary.uploader
import cloudinary.api
from django.contrib.auth.models import User

# Create your views here.
@login_required(login_url='/accounts/login/')
def home(request):
        all_posts = Post.objects.all().order_by("-created_at")
        context={'posts': all_posts}
        return render(request, 'blog/home.html', context)
     
@login_required(login_url='/accounts/login/')
def my_profile(request):
    current_user = request.user
    profile = UserProfile.objects.filter(user_id=current_user.id).first() 
    posts = Post.objects.filter(user_id=current_user.id)
    locations = Location.objects.all()
    invention_records = invention_records.objects.all()
    category = Category.objects.all()
    red_flag = red_flag.objects.filter(user_id=current_user.id)
    contacts = Contact.objects.filter(user_id=current_user.id)
    context={'profile': profile, 'posts': posts, 'locations': locations, 'invention_records': invention_records, 'categories': category, 'red_flag': red_flag, 'contacts': contacts}
    return render(request, 'blog/new_profile.html', context)

@login_required(login_url='/accounts/login/')
def update_profile_form(request):
    invention_records = invention_records.objects.all()
    locations = Location.objects.all()
    context={'locations': locations, 'invention_records': invention_records}
    return render(request, 'blog/updateProfile.html',context)

@login_required(login_url='/accounts/login/')
def update_profile(request):
    if request.method == "POST":
        current_user = request.user
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        username = request.POST["username"]
        email = request.POST["email"]
        name = request.POST["first_name"] + " " + request.POST["last_name"]
        invention_records = request.POST["invention_records"]
        location = request.POST["location"]
        if location == "":
            location = None
        else:
            location = Location.objects.get(name=location)

        if invention_records == "":
            invention_records = None
        else:
            invention_records = invention_records.objects.get(name=invention_records)
        profile_image = request.FILES["profile_pic"]
        profile_image = cloudinary.uploader.upload(profile_image)
        profile_url = profile_image["url"]
        user = User.objects.get(id=current_user.id)
        if UserProfile.objects.filter(user_id=current_user.id).exists():

            profile = UserProfile.objects.get(user_id=current_user.id)
            profile.profile_pic = profile_url
            profile.invention_records = invention_records
            profile.location = location
            profile.save()
        else:
            profile = UserProfile(user_id=current_user.id,name=name,profile_pic=profile_url,invention_records=invention_records,location=location,)

            profile.save_userProfile()

        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email

        user.save()

        return redirect("/profile",)

    else:
        return render(request, "blog/new_profile.html")


@login_required(login_url='/accounts/login/')
def addPost(request):
    locations = Location.objects.all()
    category = Category.objects.all()
    context={'locations': locations,  'categories': category}
    return render(request, 'blog/addpost.html',context)

@login_required(login_url='/accounts/login/')
def addBusiness(request):
    context={}
    return render(request, 'blog/post_detail.html',context)

@login_required(login_url='/accounts/login/')
def addContact(request):
    context={}
    return render(request, 'blog/post_form.html',context)


# create post
@login_required(login_url="/accounts/login/")
def new_post(request):
    if request.method == "POST":
        current_user = request.user
        title = request.POST["title"]
        content = request.POST["content"]
        category = request.POST["category"]
        location = request.POST["location"]
        profile = UserProfile.objects.filter(user_id=current_user.id).first()
        
        if category == "":
            category = None
        else:
            category = Category.objects.get(name=category)

        if location == "":
            location = None
        else:
            location = Location.objects.get(name=location)

        if request.FILES:
            image = request.FILES["image"]
            image = cloudinary.uploader.upload(image, crop="limit", width=800, height=600)
            image_url = image["url"]

            post = Post(user_id=current_user.id,title=title,content=content,image=image_url,category=category,location=location)
            post.save_post()

            return redirect("/profile")
        else:
            post = Post(user_id=current_user.id,title=title,content=content,category=category,location=location)
            post.save_post()

            return redirect("/profile")

    else:
        return render(request, "blog/post_form.html")


@login_required(login_url="/accounts/login/")
def save_business(request):
    if request.method == "POST":
        current_user = request.user
        name = request.POST["name"]
        email = request.POST["email"]

        profile = UserProfile.objects.filter(user_id=current_user.id).first()
        if profile is None:
            profile = UserProfile.objects.filter(
                user_id=current_user.id).first()  
            posts = Post.objects.filter(user_id=current_user.id)
            locations = Location.objects.all()
            invention_records = invention_records.objects.all()
            category = Category.objects.all()
            red_flag = red_flag.objects.filter(user_id=current_user.id)
            contacts = Contact.objects.filter(user_id=current_user.id)
            context={"locations": locations, "invention_records": invention_records, "categories": category, "red_flag": red_flag, "contacts": contacts, "posts": posts}
            return render(request, "blog/post_form.html",context)
        else:
            invention_records = profile.invention_records

        if invention_records == "":
            invention_records = None
        else:
            invention_records = invention_records.objects.get(name=invention_records)

        red_flag = red_flag(user_id=current_user.id,name=name,email=email,invention_records=invention_records,)
        invention_records.create_red_flag()

        return redirect("/profile")
    else:
        return render(request, "blog/post_form.html")


@login_required(login_url="/accounts/login/")
def save_contact(request):
    if request.method == "POST":
        current_user = request.user
        name = request.POST["name"]
        email = request.POST["email"]
        telephone = request.POST["telephone"]

        profile = UserProfile.objects.filter(user_id=current_user.id).first()
        if profile is None:
            profile = UserProfile.objects.filter(user_id=current_user.id).first() 
            posts = Post.objects.filter(user_id=current_user.id)
            locations = Location.objects.all()
            invention_records = invention_records.objects.all()
            category = Category.objects.all()
            red_flag = red_flag.objects.filter(user_id=current_user.id)
            contacts = Contact.objects.filter(user_id=current_user.id)
            context={ "locations": locations, "invention_records": invention_records, "categories": category, "red_flag": red_flag, "contacts": contacts, "posts": posts}
            return render(request, "blog/post_form.html", context)
        else:
            invention_records = profile.invention_records

        if invention_records == "":
            invention_records = None
        else:
            invention_records = invention_records.objects.get(name=invention_records)

        contact = Contact(user_id=current_user.id,name=name,email=email,telephone=telephone,invention_records=invention_records)
        contact.save_contact()

        return redirect("/profile",)
    else:
        return render(request, "blog/post_form.html")


@login_required(login_url="/accounts/login/")
def alerts(request):
    current_user = request.user
    profile = UserProfile.objects.filter(user_id=current_user.id).first()
    if profile is None:
        profile = UserProfile.objects.filter(user_id=current_user.id).first()  
        posts = Post.objects.filter(user_id=current_user.id)
        locations = Location.objects.all()
        invention_records = invention_records.objects.all()
        category = Category.objects.all()
        red_flag = red_flag.objects.filter(user_id=current_user.id)
        contacts = Contact.objects.filter(user_id=current_user.id)
        context= {"locations": locations, "invention_records": invention_records, "categories": category, "red_flag": red_flag, "contacts": contacts, "posts": posts}
        return render(request, "blog/post_form.html",context)
    else:
        invention_records = profile.invention_records
        category = Category.objects.get(name="alerts")
        posts = Post.objects.filter(invention_records=invention_records, category=category).order_by("-created_at")
        context={"posts": posts}
        return render(request, "blog/post_form.html", context)


@login_required(login_url="/accounts/login/")
def red_flag(request):
    current_user = request.user
    profile = UserProfile.objects.filter(user_id=current_user.id).first()
    if profile is None:
        profile = UserProfile.objects.filter(
            user_id=current_user.id).first() 
        posts = Post.objects.filter(user_id=current_user.id)
        locations = Location.objects.all()
        invention_records = invention_records.objects.all()
        category = Category.objects.all()
        red_flag = red_flag.objects.filter(user_id=current_user.id)
        contacts = Contact.objects.filter(user_id=current_user.id)
        context= {"locations": locations, "invention_records": invention_records, "categories": category, "red_flag": red_flag, "contacts": contacts, "posts": posts}
        return render(request, "blog/post_form.html",context)
    else:
        invention_records = profile.invention_records
        red_flag = red_flag.objects.filter(invention_records=profile.invention_records)
        context={"red_flag": red_flag}
        return render(request, "blog/post_form.html", context)


@login_required(login_url="/accounts/login/")
def contacts(request):
    current_user = request.user
    profile = UserProfile.objects.filter(user_id=current_user.id).first()
    
    contacts = Contact.objects.all()
    context= {"contacts": contacts, "invention_records": profile.invention_records}
    return render(request, "blog/post_form.html",context)


@login_required(login_url="/accounts/login/")
def search(request):
    if 'query' in request.GET and request.GET["query"]:
        search_term = request.GET.get("query")
        searched_red_flag = red_flag.objects.filter(name__icontains=search_term)
        message = f"Search For: {search_term}"
        context={"message": message, "red_flag": searched_red_flag}
        return render(request, "blog/post_form.html", context)
    else:
        message = "You haven't searched for any term"
        context= {"message": message}
        return render(request, "blog/post_detail.html",context)
