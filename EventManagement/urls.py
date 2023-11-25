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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.events_list, name='events_list'),
    path('create_conference/', views.create_conference, name='create_conference'),
    path('edit_conference/<int:pk>/', views.edit_conference, name='edit_conference'),
    path('delete_conference/<int:pk>/', views.delete_conference, name='delete_conference'),
    path('create_workshop/', views.create_workshop, name='create_workshop'),
    path('edit_workshop/<int:pk>/', views.edit_workshop, name='edit_workshop'),
    path('create_social_event/', views.create_social_event, name='create_social_event'),
    path('edit_social_event/<int:pk>/', views.edit_social_event, name='edit_social_event'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
