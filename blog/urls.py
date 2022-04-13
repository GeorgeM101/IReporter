from django.urls import path
from blog import views
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView
from django.urls import path,re_path
from . import views


urlpatterns = [
    path('about/', views.about, name="blog-about"),
    path('', PostListView.as_view(), name="blog-home"),
    path('post-new/', PostCreateView.as_view(), name="blog-new"),
    path('post/<int:pk>/', PostDetailView.as_view(), name="blog-detail"),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name="blog-update"),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name="blog-delete"),
    path('video/', views.video, name="video"),
    path('',views.home,name="home"),
    path("profile/", views.my_profile, name="profile"),
    path("profile/updateprofile/", views.update_profile_form, name="updateprofileform"), 
    path("profile/update/", views.update_profile, name="updateprofile"), 
    path("addpost/", views.addPost, name="addpost"),
    path("addbusiness/", views.addBusiness, name="addbusiness"),
    path("addcontact/", views.addContact, name="addcontact"),
    path("post/save/", views.new_post, name="save_new_post"),
    path("business/save/", views.save_business, name="save_new_business"),
    path("contact/save/", views.save_contact, name="save_new_contact"),
    path("notifications/", views.alerts, name="alerts"), 
    path("business/", views.business, name="business"), 
    path("contacts/", views.contacts, name="contacts"), 
    path("search/", views.search, name="search"),

]
