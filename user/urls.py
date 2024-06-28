from . import views
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
    path("job-list/", views.job_list, name="job-list"),

    path('category/', views.category, name="category"),
   # path("job-detail/", views.job_detail, name="job-detail"),
    path('navbar/', views.navbar, name="navbar"),
    path("testimonial/", views.testimonial, name="testimonial"),
    path("viewcard/", views.viewcard, name="viewcard"),

    path("about/", views.about, name="about"),
    path('registration/', views.registration, name='registration'),
	path('profile_update/', views.updateProfile, name="profile_update"),
	path('balance/', views.balance, name="balance"),
	path('profile/', views.profile, name="profile"),

    path('delete_post/<int:post_id>/', views.deletePost, name='delete_post'),
    path('contact/<int:post_id>/', views.contact, name='contact'),

	path('post/', views.post, name="post"),
	path('create_post/', views.createPost, name="create_post"),
	path('update_post/', views.updatePost, name="update_post"),
	path('send_email/', views.sendEmail, name="send_email"),
    path('buy-card/<int:post_id>/', views.buy_card, name='buy_card'),
    path('job-detail/<int:post_id>/', views.job_detail, name='job-detail'),
]


