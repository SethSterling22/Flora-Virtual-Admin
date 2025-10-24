from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login, logout

from django.urls import reverse

# Extra Modules
from django.contrib.auth.models import User
from .validator import CustomPasswordValidator


# Token Modules
from django.contrib.auth.tokens import default_token_generator
from rest_framework.authtoken.models import Token



@csrf_protect
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Busca al usuario por el correo electrónico
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if user and user.check_password(password):
            login(request, user) # Crea la sesión
            token, created = Token.objects.get_or_create(user=user)  # Crea o obtiene el token
            request.session['user_token'] = token.key  # Guarda el token en la sesión
            return redirect(f"{reverse('main:content')}?item=Familias")

        else:
            messages.error(request, "Correo electrónico o contraseña incorrecta.")
            return redirect('login:login')

    return render(request, 'login.html')




@csrf_protect
def logout_user(request):
    user_token = request.session.get('user_token')
    if user_token:
        try:
            token = Token.objects.get(key=user_token)
            token.delete()  # Elimina el token de la base de datos
        except Token.DoesNotExist:
            pass

    logout(request)  # Cierra la sesión
    return redirect('login:login')  

