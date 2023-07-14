from django.contrib import admin
from django.urls import path, include
from . import views 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name = 'index'),
    path('signup', views.signup, name='signup'),
    path('signout', views.signout, name='signout'),
    path('signin', views.signin, name='signin'),
    path('main', views.main, name='main')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



