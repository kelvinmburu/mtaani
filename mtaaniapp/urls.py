from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', views.index, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.signup, name='register'),
    path('contact/', views.contact, name='contact'),
    path('support/', views.support, name='support'),
    
    path('', views.home, name='home'),
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
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)