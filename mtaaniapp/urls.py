from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('index/', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('contact/', views.contact, name='contact'),
    path('account/', include('django.contrib.auth.urls')),
    path('all_hoods/', views.hoods, name='hood'),
    path('new_hood/', views.create_hood, name='new_hood'),
    path('profile/<username>', views.profile, name='profile'),
    path('profile/<username>/edit/', views.edit_profile, name='edit-profile'),
    path('join_hood/<id>', views.join_hood, name='join-hood'),
    path('leave_hood/<id>', views.leave_hood, name='leave-hood'),
    path('single_hood/<hood_id>', views.single_hood, name='single-hood'),
    path('<hood_id>/new-post', views.create_post, name='post'),
    path('<hood_id>/members', views.hood_members, name='members'),
    path('search/', views.search_business, name='search'),
]