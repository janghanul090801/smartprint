from django.urls import path
from django.conf import settings
from . import views
from django.conf.urls.static import static

app_name = 'order'

urlpatterns = [
    path('orderCart/',views.OrderCartView.as_view(), name='orderCart'),
    path('orderDetails/',views.orderDetails, name='orderDetails'),
    path('orderInfo/', views.orderInfo, name="orderInfo"),
    path('orderForm/', views.orderForm, name="orderForm"),
    path('submissionForm/<str:category>/<int:id>/',views.SubmissionFormView.as_view(), name="submissionForm"),
    path('showProduct/<str:category>/', views.showProduct, name="showProduct"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)