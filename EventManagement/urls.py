"""
URL configuration for EventManagement project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Event import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.events_list, name='events_list'),

    #auth
    path("signup/",views.signup, name ='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(), name='logout'),


    #oprations
    path('create_conference/', views.create_conference, name='create_conference'),
    path('edit_conference/<int:pk>/', views.edit_conference, name='edit_conference'),
    path('delete_conference/<int:pk>/', views.delete_conference, name='delete_conference'),
    path('create_workshop/', views.create_workshop, name='create_workshop'),
    path('edit_workshop/<int:pk>/', views.edit_workshop, name='edit_workshop'),
    path('delete_workshop/<int:pk>/', views.delete_workshop, name='delete_workshop'),
    path('create_social_event/', views.create_social_event, name='create_social_event'),
    path('edit_social_event/<int:pk>/', views.edit_social_event, name='edit_social_event'),
    path('delete_social_event/<int:pk>/', views.delete_social_event, name='delete_social_event'),
    path('locations/', views.location_list, name='location_list'),
    path('edit_location/<int:location_id>/', views.edit_location, name="edit_location"),
    path('delete_location/<int:location_id>/', views.delete_location, name = "delete_location"),



    #queries
    path('draft_event/', views.draft_event, name= "draft_event"),
    path('completed_events/', views.completed_events, name = "completed_events"), 
    path('cancelled_events/', views.cancelled_events, name="cancelled_events"),
    path('create_location/', views.create_location, name = "create_location"),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
