from django.urls import path



from django.conf import settings
from django.conf.urls.static import static


from login.views import *
from main.views import main_page


app_name = 'login'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_user, name='logout'),
    # path('dashboard/', main_page, name='dashboard'),
]
