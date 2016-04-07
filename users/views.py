from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout

from users.models import User
from users.forms import UserForm

# Create your views here.
class Register(View):
    def post(self, request):
        data = request.POST
        username = data.get('username')
        password1 = data.get('password1')
        password2 = data.get('password2')

        if not (username and password1 and password2):
            return JsonResponse({'Message':'Missing username or password.'})
        if password1 != password2:
            return JsonResponse({'Message': 'Passwords do not match.'})
        user = User.objects.filter(username=username)

        if user:
            return JsonResponse({'Message':'That username already exits.'})
        user = User.objects.create(username=username,password=password1)
        return JsonResponse({'success': True,'Message':'user created please login'})

class Login(View):
    def post(self, request):
        data = request.POST
        username = data.get('username')
        password = data.get('password')

        if not (username and password):
            return JsonResponse({'Message':'Missing username or password.'})
        user_set = User.objects.filter(username=username,password=password)

        if not user_set:
            return JsonResponse({'Message':'Invalid `username` or `password`.'})
        user = user_set[0]
        return JsonResponse({'success':True,'access_token': user.access_token})

class Logout(View):
    def post(self, request):        
        if request.is_ajax():
            content = request.POST
        else:
            body = request.body.decode()
            if not body: 
                return JsonResponse ({"response":"Missing Body"})
            content = json.loads(body)

        token = content.get("token")
        user = User.objects.get(access_token = token)
        logout(request)

        if user:
            return JsonResponse ({"response":"Logout Successful"})
        else:
            return JsonResponse ({"response":"Invalid username or password"})

