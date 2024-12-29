from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

# app_name='sns'

urlpatterns = [
    path('', views.top, name='top'),
    path('index', views.index, name='index'),
    path('index/<int:page>/', views.index, name='index'),
    path('post', views.post, name='post'),
    path('delete/<int:num>', views.delete, name='delete'),
    path('edit/<int:num>', views.edit, name='edit'),
    path('comment', views.comment, name='comment'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)