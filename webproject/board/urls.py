from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'board'

urlpatterns = [
    path('notice/', views.notice, name='notice'),
    path('faq/', views.faq, name="faq"),
    path('postView/<int:id>/', views.postView, name="postView"),
    path('postWrite/<str:category>/', views.postWrite, name="postWrite"),
    path('quoteInquiry/', views.quoteInquiry, name="quoteInquiry"),
    path('quoteWrite/', views.quoteWrite, name='quoteWrite'),
    path('quoteView/<int:id>/', views.quoteView, name='quoteView'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 