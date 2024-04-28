from . import views
from django.conf.urls import url
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url('$', views.home, name=''),
    url(r'^job-list/', views.job_list, name='job-list'),
    url(r'^job-detail/', views.job_detail, name='job-detail'),

    path('category/', views.category, name="category"),

    url(r'^testimonial/', views.testimonial, name='testimonial'),
    url(r'^navbar/', views.navbar, name='navbar'),
    path("about/", views.about, name="about"),
    url(r'^home/', views.home, name='home'),
    path('registration/', views.registration, name='registration'),
	path('profile_update/', views.updateProfile, name="profile_update"),
	path('post-job/', views.postjob, name="post"),

    url(r'^profile/', views.profile, name='profile'),
    path('delete_post/<int:post_id>/', views.deletePost, name='delete_post'),
    path('contact/<int:post_id>/', views.contact, name='contact'),

	path('post/', views.post, name="post"),
	path('create_post/', views.createPost, name="create_post"),
	path('update_post/', views.updatePost, name="update_post"),
	path('send_email/', views.sendEmail, name="send_email"),

]