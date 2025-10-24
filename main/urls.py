from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from main.views import *

from main.methods import *

app_name = 'main' 

urlpatterns = [
    # path('dashboard/', main_page, name='dashboard'),
    path('content/', content_view, name='content'),

    path('add/', add, name='add'),
    path('delete/<int:id>/<str:title>/', delete, name='delete'),
    path('update/', update, name='update'),
]