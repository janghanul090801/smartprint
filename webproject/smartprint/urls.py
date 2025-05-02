from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'smartprint'

urlpatterns = [
    path('',views.home,name='home'),
    path('terms',views.terms,name='terms'),
    path('privacy',views.privacy,name='privacy'),
    path('direction', views.direction, name='direction')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

